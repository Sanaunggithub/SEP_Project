from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.auth import User
from models.grade import Grade, GPA
from models.schemas import GradeSchema, GradeCreate, GPASchema
from core.security import get_current_user

router = APIRouter(prefix="/grades", tags=["grades"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/", response_model=list[GradeSchema])
def list_grades(
    student_id: str | None = Query(None),
    course_id: str | None = Query(None),
    semester: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Grade)
    
    if student_id:
        if current_user.role.value not in ["admin", "instructor"] and str(current_user.id) != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        query = query.filter(Grade.student_id == student_id)
    
    if course_id:
        query = query.filter(Grade.course_id == course_id)
    
    if semester:
        query = query.filter(Grade.semester == semester)
    
    grades = query.offset(skip).limit(limit).all()
    return grades

@router.post("/", response_model=GradeSchema, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.put("/{grade_id}", response_model=GradeSchema)
def update_grade(
    grade_id: str,
    grade_update: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    
    db.delete(grade)
    db.commit()

@router.get("/gpa/{student_id}", response_model=list[GPASchema])
def get_student_gpa(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.value not in ["admin"] and str(current_user.id) != student_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    gpas = db.query(GPA).filter(GPA.student_id == student_id).all()
    return gpas

@router.get("/report/{course_id}")
def get_grade_distribution(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    grades = db.query(Grade).filter(Grade.course_id == course_id).all()
    
    if not grades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No grades found for this course")
    
    scores = [g.score for g in grades]
    return {
        "course_id": course_id,
        "total_students": len(grades),
        "average_score": sum(scores) / len(scores),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "median_score": sorted(scores)[len(scores) // 2]
    }
