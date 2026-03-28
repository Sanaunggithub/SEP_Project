from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.attendance import Attendance
from schemas.attendance import AttendanceCreate, AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/", response_model=AttendanceResponse)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/", response_model=list[AttendanceResponse])
def read_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()
