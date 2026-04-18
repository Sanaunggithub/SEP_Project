from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta, date
from database import get_db
from models.auth import User
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import UserCreate, UserResponse, UserUpdate, RoleEnum
from core.security import create_access_token, hash_password, verify_password, get_current_user
from core.config import settings
from models.course import Course, CourseEnrollment, CourseStatus
from models.student import Student

router = APIRouter(prefix="/auth", tags=["auth"])
import uuid

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        full_name                = user_data.full_name,
        email                    = user_data.email,
        hashed_password          = hash_password(user_data.password),
        role                     = user_data.role,
        phone_number             = user_data.phone_number,
        date_of_birth            = user_data.date_of_birth,
        gender                   = user_data.gender,
        address                  = user_data.address,
        emergency_contact_name   = user_data.emergency_contact_name,
        emergency_contact_phone  = user_data.emergency_contact_phone,
        is_active                = True
    )
    db.add(new_user)
    db.flush()  # get new_user.id without committing yet

    # Auto-create Student profile if role is student
    if user_data.role == RoleEnum.student:
        student_number = f"STU-{str(new_user.id)[:8].upper()}"
        new_student = Student(
            user_id           = new_user.id,
            student_id_number = student_number,
            enrollment_date   = date.today(),
            department        = user_data.department or "Undeclared",  # ← fixed
            program           = user_data.program    or "Undeclared",  # ← fixed
            year_level        = 1,
            academic_status   = "active",
            scholarship_status = False
        )
        db.add(new_student)

    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/majors/")
def get_majors(db: Session = Depends(get_db)):
    # Get all unique departments from students
    # Exclude "Undeclared" from public majors list
    departments = db.query(Student.department)\
        .filter(
            Student.is_active  == True,
            Student.department != "Undeclared",
            Student.department != "",
            Student.department.isnot(None)
        )\
        .distinct().all()
    departments = [d.department for d in departments if d.department]

    result = []
    for dept in departments:
        student_count = db.query(Student)\
            .filter(Student.department == dept, Student.is_active == True)\
            .count()

        enrolled_course_ids = db.query(CourseEnrollment.course_id)\
            .join(Student, CourseEnrollment.student_id == Student.id)\
            .filter(Student.department == dept)\
            .distinct().subquery()

        lecturer_count = db.query(Course.instructor_id)\
            .filter(Course.id.in_(enrolled_course_ids))\
            .distinct().count()

        course_count = db.query(Course)\
            .filter(
                Course.id.in_(enrolled_course_ids),
                Course.is_active == True
            ).count()

        result.append({
            "name":            dept,
            "total_students":  student_count,
            "total_lecturers": lecturer_count,
            "total_courses":   course_count
        })

    return result

@router.get("/stats/public")
def get_public_stats(db: Session = Depends(get_db)):
    student_count  = db.query(User).filter(
        User.role == "student",    User.is_active == True).count()
    lecturer_count = db.query(User).filter(
        User.role == "instructor", User.is_active == True).count()
    course_count   = db.query(Course).filter(
        Course.is_active == True,
        Course.status    == CourseStatus.active
    ).count()

    return {
        "total_students":  student_count,
        "total_courses":   course_count,
        "total_lecturers": lecturer_count
    }

@router.get("/instructors/public")
def get_public_instructors(db: Session = Depends(get_db)):
    instructors = db.query(User).filter(
        User.role      == "instructor",
        User.is_active == True
    ).all()
    return [{"id": str(u.id), "full_name": u.full_name} for u in instructors]

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type":   "bearer",
        "user":         UserResponse.from_orm(user)
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_profile(
    profile_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users", response_model=list[UserResponse])
def list_users(
    role:  str | None = None,
    skip:  int        = 0,
    limit: int        = Query(100, le=1000),
    db:    Session    = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    query = db.query(User).filter(User.is_active == True)
    if role:
        query = query.filter(User.role == role)
    return query.offset(skip).limit(limit).all()

@router.post("/upload-profile-picture")
def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import os
    from core.config import settings

    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

    file_path = f"{settings.UPLOAD_DIR}/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    user = db.query(User).filter(User.id == current_user.id).first()
    user.profile_picture_url = file_path
    db.add(user)
    db.commit()

    return {"filename": file.filename, "profile_picture_url": file_path}