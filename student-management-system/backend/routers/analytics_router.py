from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.auth import User
from models.course import Course, CourseEnrollment
from models.attendance import Attendance
from models.grade import Grade
from models.analytics import ReportSnapshot
from schemas.analytics import ReportSnapshotCreate, ReportSnapshotResponse
from core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/enrollment-trends")
def get_enrollment_trends(
    semester: str | None = Query(None),
    year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))
):
    query = db.query(Course)
    
    if semester:
        query = query.filter(Course.semester == semester)
    if year:
        query = query.filter(Course.year == year)
    
    courses = query.all()
    
    return {
        "total_courses": len(courses),
        "total_enrolled": sum(c.enrolled_count for c in courses),
        "average_enrollment": sum(c.enrolled_count for c in courses) / len(courses) if courses else 0,
        "courses_at_capacity": len([c for c in courses if c.enrolled_count >= c.max_seats])
    }

@router.get("/attendance-patterns")
def get_attendance_patterns(
    course_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))
):
    query = db.query(Attendance)
    if course_id:
        query = query.filter(Attendance.course_id == course_id)
    
    attendance_data = query.all()
    
    if not attendance_data:
        return {"message": "No attendance data available"}
    
    from collections import Counter
    status_counts = Counter(a.status.value for a in attendance_data)
    
    return {
        "total_records": len(attendance_data),
        "status_distribution": dict(status_counts),
        "average_attendance_percentage": sum(a.attendance_percentage or 0 for a in attendance_data) / len(attendance_data)
    }

@router.get("/grade-distribution")
def get_grade_distribution(
    course_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))
):
    query = db.query(Grade)
    if course_id:
        query = query.filter(Grade.course_id == course_id)
    
    grades = query.all()
    
    if not grades:
        return {"message": "No grade data available"}
    
    scores = [g.score for g in grades]
    return {
        "total_grades": len(grades),
        "average_score": sum(scores) / len(scores),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "median_score": sorted(scores)[len(scores) // 2],
        "std_deviation": (sum((x - sum(scores) / len(scores)) ** 2 for x in scores) / len(scores)) ** 0.5
    }

@router.get("/student-performance/{student_id}")
def get_student_performance(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.value not in ["admin"] and str(current_user.id) != student_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    enrollments = db.query(CourseEnrollment).filter(CourseEnrollment.student_id == student_id).all()
    attendance = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    
    avg_grade = sum(g.score for g in grades) / len(grades) if grades else 0
    avg_attendance = sum(a.attendance_percentage or 0 for a in attendance) / len(attendance) if attendance else 0
    
    return {
        "student_id": student_id,
        "courses_enrolled": len(enrollments),
        "average_grade": avg_grade,
        "total_grades": len(grades),
        "average_attendance": avg_attendance,
        "attendance_records": len(attendance)
    }

@router.post("/generate-report", response_model=ReportSnapshotResponse, status_code=status.HTTP_201_CREATED)
def generate_report(
    report: ReportSnapshotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))
):
    db_report = ReportSnapshot(**report.dict(), generated_by=current_user.id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/reports", response_model=list[ReportSnapshotCreate])
def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    reports = db.query(ReportSnapshot).offset(skip).limit(limit).all()
    return reports

@router.get("/reports/{report_id}/export")
def export_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    report = db.query(ReportSnapshot).filter(ReportSnapshot.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    return {
        "report_id": report_id,
        "export_format": report.export_format.value,
        "message": f"Export prepared as {report.export_format.value}",
        "data": report.result_summary
    }
