from fastapi import FastAPI
from routers import student_router, course_router, grade_router, attendance_router, assignment_router, notification_router, analytics_router, auth_router
from database import engine
from models import Base
from models import Student, Course, Grade, Attendance, Assignment, Notification, Analytics

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(student_router.router)
app.include_router(course_router.router)
app.include_router(grade_router.router)
app.include_router(attendance_router.router)
app.include_router(assignment_router.router)
app.include_router(notification_router.router)
app.include_router(analytics_router.router)
app.include_router(auth_router.router)
