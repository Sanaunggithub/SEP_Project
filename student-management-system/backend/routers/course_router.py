from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.course import Course
from schemas.course import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=list[CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
