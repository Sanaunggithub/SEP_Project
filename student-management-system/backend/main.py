from fastapi import FastAPI
from routers import student_router, course_router, grade_router, attendance_router, assignment_router, analytics_router, auth_router
from database import engine
from models.base import Base
from models.auth import User
from models.student import Student
from models.course import Course, CourseEnrollment
from models.grade import Grade
from models.attendance import Attendance
from models.assignment import Assignment, Submission
from models.analytics import ReportSnapshot
from models.attendance import Attendance 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(student_router.router)
app.include_router(course_router.router)
app.include_router(grade_router.router)
app.include_router(attendance_router.router)
app.include_router(assignment_router.router)
app.include_router(analytics_router.router)
app.include_router(auth_router.router)
