from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
