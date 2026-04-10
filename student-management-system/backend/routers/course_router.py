from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.auth import User, Role
from models.course import Course, CourseEnrollment, CourseStatus
from schemas.course import CourseResponse, CourseCreate, CourseUpdate, EnrollmentResponse
from core.security import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/", response_model=list[CourseResponse])
def list_courses(
    semester: str | None = Query(None),
    department: str | None = Query(None),
    status_filter: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(Course).filter(Course.is_active == True)
    
    if semester:
        query = query.filter(Course.semester == semester)
    if department:
        query = query.filter(Course.department == department)
    if status_filter:
        query = query.filter(Course.status == status_filter)
    
    courses = query.offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    existing_course = db.query(Course).filter(Course.course_code == course.course_code).first()
    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code already exists")
    
    course_data = course.dict(exclude_none=True)
    db_course = Course(**course_data)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: str,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if current_user.role.value == "instructor" and str(course.instructor_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    update_data = course_update.dict(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if current_user.role.value == "instructor" and str(course.instructor_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    course.is_active = False
    db.add(course)
    db.commit()

@router.post("/{course_id}/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(
    course_id: str,
    student_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    role = current_user.role.value

    # Role-based access control
    if role == "instructor":
        # Instructor can only enroll into their own courses
        if str(course.instructor_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="You can only enroll students in your own courses")

    elif role == "student":
        # Student can only enroll themselves
        from models.student import Student
        own_student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not own_student or str(own_student.id) != str(student_id):
            raise HTTPException(status_code=403, detail="You can only enroll yourself")

    # Check capacity
    if course.enrolled_count >= course.max_seats:
        raise HTTPException(status_code=400, detail="No seats available")

    # Check duplicate
    existing = db.query(CourseEnrollment).filter(
        CourseEnrollment.student_id == student_id,
        CourseEnrollment.course_id == course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    enrollment = CourseEnrollment(student_id=student_id, course_id=course_id)
    course.enrolled_count += 1
    db.add(enrollment)
    db.add(course)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.delete("/{course_id}/enroll", status_code=status.HTTP_204_NO_CONTENT)
def drop_course(
    course_id: str,
    student_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.student_id == student_id,
        CourseEnrollment.course_id == course_id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    
    course = db.query(Course).filter(Course.id == course_id).first()
    course.enrolled_count = max(0, course.enrolled_count - 1)
    
    db.delete(enrollment)
    db.add(course)
    db.commit()

@router.get("/{course_id}/students")
def get_enrolled_students(
    course_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if current_user.role.value == "instructor" and str(course.instructor_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).offset(skip).limit(limit).all()
    return [enrollment.student for enrollment in enrollments]

@router.get("/{course_id}/schedule")
def get_course_schedule(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return {
        "course_id": course_id,
        "schedule_days": course.schedule_days,
        "start_time": course.start_time,
        "end_time": course.end_time,
        "room_location": course.room_location
    }
