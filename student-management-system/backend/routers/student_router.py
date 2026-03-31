from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User, Role
from models.student import Student
from models.course import CourseEnrollment
from models.grade import Grade
from models.attendance import Attendance
from schemas.student import StudentResponse, StudentCreate, StudentUpdate
from core.security import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/", response_model=list[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    students = db.query(Student).filter(Student.is_active == True).offset(skip).limit(limit).all()
    result = []
    for student in students:
        student_data = StudentResponse.model_validate(student)
        student_data.full_name = student.user.full_name if student.user else None
        result.append(student_data)
    
    return result

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if current_user.role.value != "admin" and str(current_user.id) != str(student.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    student_data = StudentResponse.model_validate(student)
    student_data.full_name = student.user.full_name if student.user else None
    return student_data

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    existing_student = db.query(Student).filter(Student.student_id_number == student.student_id_number).first()
    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student ID already exists")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    student_data = StudentResponse.model_validate(db_student)
    student_data.full_name = db_student.user.full_name if db_student.user else None
    return student_data

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    update_data = student_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    student_data = StudentResponse.model_validate(student)
    student_data.full_name = student.user.full_name if student.user else None
    return student_data

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    student.is_active = False
    db.add(student)
    db.commit()

@router.get("/{student_id}/courses")
def get_student_courses(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if current_user.role.value != "admin" and str(current_user.id) != str(student.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    enrollments = db.query(CourseEnrollment).filter(CourseEnrollment.student_id == student_id).offset(skip).limit(limit).all()
    return [{"course": enrollment.course, "status": enrollment.status.value, "enrolled_at": enrollment.enrolled_at} for enrollment in enrollments]

@router.get("/{student_id}/grades")
def get_student_grades(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if current_user.role.value != "admin" and str(current_user.id) != str(student.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    grades = db.query(Grade).filter(Grade.student_id == student_id).offset(skip).limit(limit).all()
    return grades

@router.get("/{student_id}/attendance")
def get_student_attendance(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if current_user.role.value != "admin" and str(current_user.id) != str(student.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    attendance = db.query(Attendance).filter(Attendance.student_id == student_id).offset(skip).limit(limit).all()
    return attendance
