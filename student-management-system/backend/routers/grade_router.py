from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.grade import Grade
from schemas.grade import GradeCreate, GradeResponse

router = APIRouter(prefix="/grades", tags=["grades"])

@router.post("/", response_model=GradeResponse)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/", response_model=list[GradeResponse])
def read_grades(db: Session = Depends(get_db)):
    return db.query(Grade).all()
