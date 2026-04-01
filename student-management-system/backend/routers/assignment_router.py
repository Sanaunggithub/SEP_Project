from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.auth import User
from models.assignment import Assignment, Submission
from schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse, SubmissionCreate, SubmissionUpdate, SubmissionResponse
from core.security import get_current_user
import os
from core.config import settings

router = APIRouter(prefix="/assignments", tags=["assignments"])

class RoleChecker:
    def __init__(self, required_roles: list):
        self.required_roles = required_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        role_val = current_user.role.value if hasattr(current_user.role, 'value') else current_user.role
        if role_val not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Your role: {role_val}"
            )
        return current_user

@router.get("/", response_model=list[AssignmentResponse])
def list_assignments(
    course_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Assignment)
    if course_id:
        query = query.filter(Assignment.course_id == course_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["instructor", "admin"]))
):
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: str,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["instructor", "admin"]))
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    
    for field, value in assignment_update.dict(exclude_unset=True).items():
        setattr(assignment, field, value)
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin"]))
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    
    db.delete(assignment)
    db.commit()

@router.post("/{assignment_id}/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_assignment(
    assignment_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["student"]))
):
    from models.student import Student

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

    file_path = f"{settings.UPLOAD_DIR}/{assignment_id}_{student.id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    is_late = datetime.now() > assignment.due_date if assignment.due_date else False

    submission = Submission(
        student_id=student.id,
        assignment_id=assignment_id,
        file_url=file_path,
        is_late=is_late
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

@router.get("/{assignment_id}/submissions")
def get_assignment_submissions(
    assignment_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["instructor", "admin"]))
):
    return db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).offset(skip).limit(limit).all()

@router.put("/submissions/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(
    submission_id: str,
    grade_update: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["instructor", "admin"]))
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    for field, value in grade_update.dict(exclude_unset=True).items():
        setattr(submission, field, value)

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

@router.get("/submissions/{submission_id}")
def get_student_submission(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    role_val = current_user.role.value if hasattr(current_user.role, 'value') else current_user.role
    if role_val not in ["admin", "instructor"] and str(current_user.id) != str(submission.student_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    return submission