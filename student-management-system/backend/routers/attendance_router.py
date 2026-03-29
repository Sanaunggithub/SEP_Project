from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from database import get_db
from models.auth import User
from models.attendance import Attendance
from models.schemas import AttendanceSchema, AttendanceCreate
from core.security import get_current_user

router = APIRouter(prefix="/attendance", tags=["attendance"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.post("/", response_model=AttendanceSchema, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    existing = db.query(Attendance).filter(
        and_(
            Attendance.student_id == attendance.student_id,
            Attendance.course_id == attendance.course_id,
            Attendance.date == attendance.date
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attendance already marked")
    
    db_attendance = Attendance(**attendance.dict(), marked_by=current_user.id)
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/{course_id}")
def get_course_attendance(
    course_id: str,
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    query = db.query(Attendance).filter(Attendance.course_id == course_id)
    
    if date_from:
        query = query.filter(Attendance.date >= date_from)
    if date_to:
        query = query.filter(Attendance.date <= date_to)
    
    attendance = query.offset(skip).limit(limit).all()
    return attendance

@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: str,
    course_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.value not in ["admin"] and str(current_user.id) != student_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    query = db.query(Attendance).filter(Attendance.student_id == student_id)
    if course_id:
        query = query.filter(Attendance.course_id == course_id)
    
    attendance = query.offset(skip).limit(limit).all()
    return attendance

@router.put("/{attendance_id}", response_model=AttendanceSchema)
def correct_attendance(
    attendance_id: str,
    status_update: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    attendance.status = status_update
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/at-risk")
def get_at_risk_students(
    threshold: float = Query(75.0, ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    from sqlalchemy import func
    
    at_risk = db.query(
        Attendance.student_id,
        func.avg(Attendance.attendance_percentage).label("avg_attendance")
    ).group_by(Attendance.student_id).having(
        func.avg(Attendance.attendance_percentage) < threshold
    ).all()
    
    return [{"student_id": record[0], "average_attendance": record[1]} for record in at_risk]

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def bulk_mark_attendance(
    records: list[AttendanceCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    attendance_records = [Attendance(**record.dict(), marked_by=current_user.id) for record in records]
    db.add_all(attendance_records)
    db.commit()
    return {"message": f"{len(attendance_records)} attendance records marked"}
