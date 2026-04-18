from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.auth import User
from models.grade import Grade, GPA
from schemas.grade import GradeResponse, GradeCreate, GradeUpdate, GPAResponse, GradeDistributionResponse
from core.security import get_current_user
from models.course import CourseEnrollment
from models.student import Student

router = APIRouter(prefix="/grades", tags=["grades"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

@router.get("/", response_model=list[GradeResponse])
def list_grades(
    student_id: str | None = Query(None),
    course_id: str | None = Query(None),
    semester: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Grade)

    if student_id:
        if current_user.role.value not in ["admin", "instructor"] and \
           str(current_user.id) != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized"
            )
        query = query.filter(Grade.student_id == student_id)

    if course_id:
        query = query.filter(Grade.course_id == course_id)

    if semester:
        query = query.filter(Grade.semester == semester)

    grades = query.offset(skip).limit(limit).all()
    return grades

@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))  # ← fixed: use check_role
):
    # Check student is enrolled in this course
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.student_id == grade.student_id,
        CourseEnrollment.course_id  == grade.course_id
    ).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in this course"
        )

    # Check if this component already graded for this student in this course
    existing = db.query(Grade).filter(
        Grade.student_id     == grade.student_id,
        Grade.course_id      == grade.course_id,
        Grade.component_type == grade.component_type
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Grade for '{grade.component_type}' already exists for this student "
                   f"in this course. Use edit to update it."
        )

    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
    grade_id: str,
    grade_update: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    update_data = grade_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(grade, field, value)

    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    db.delete(grade)
    db.commit()

@router.get("/{student_id}/grades")
def get_student_grades(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user.role.value != "admin" and str(current_user.id) != str(student.user_id):
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Return all grades including those from deleted courses
    grades = db.query(Grade).filter(
        Grade.student_id == student_id
    ).offset(skip).limit(limit).all()
    return grades

@router.get("/gpa/{student_id}")
def get_student_gpa(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from models.student import Student

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if current_user.role.value not in ["admin", "instructor"] and \
       str(current_user.id) != str(student.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )

    return {"student_id": student_id, "gpa": student.gpa}

@router.get("/report/{course_id}")
def get_grade_distribution(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    grades = db.query(Grade).filter(Grade.course_id == course_id).all()

    if not grades:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No grades found for this course"
        )

    scores = [g.score for g in grades]
    return {
        "course_id":      course_id,
        "total_students": len(grades),
        "average_score":  sum(scores) / len(scores),
        "highest_score":  max(scores),
        "lowest_score":   min(scores),
        "median_score":   sorted(scores)[len(scores) // 2]
    }

