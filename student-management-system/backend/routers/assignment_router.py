from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.auth import User
from models.assignment import Assignment, Submission
from models.schemas import AssignmentSchema, AssignmentCreate, AssignmentUpdate, SubmissionSchema, SubmissionCreate, SubmissionUpdate
from core.security import get_current_user

router = APIRouter(prefix="/assignments", tags=["assignments"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/", response_model=list[AssignmentSchema])
def list_assignments(
    course_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Assignment)
    if course_id:
        query = query.filter(Assignment.course_id == course_id)
    
    assignments = query.offset(skip).limit(limit).all()
    return assignments

@router.post("/", response_model=AssignmentSchema, status_code=status.HTTP_201_CREATED)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/{assignment_id}", response_model=AssignmentSchema)
def update_assignment(
    assignment_id: str,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    
    update_data = assignment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    
    db.delete(assignment)
    db.commit()

@router.post("/{assignment_id}/submit", response_model=SubmissionSchema, status_code=status.HTTP_201_CREATED)
def submit_assignment(
    assignment_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["student"]))
):
    import os
    from core.config import UPLOAD_DIR
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = f"{UPLOAD_DIR}/{assignment_id}_{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    is_late = datetime.now() > assignment.due_date if assignment.due_date else False
    
    submission = Submission(
        student_id=current_user.id,
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
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    submissions = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).offset(skip).limit(limit).all()
    return submissions

@router.put("/submissions/{submission_id}/grade", response_model=SubmissionSchema)
def grade_submission(
    submission_id: str,
    grade_update: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["instructor", "admin"]))
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    
    update_data = grade_update.dict(exclude_unset=True)
    for field, value in update_data.items():
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
    
    if current_user.role.value not in ["admin", "instructor"] and str(current_user.id) != str(submission.student_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    return submission
