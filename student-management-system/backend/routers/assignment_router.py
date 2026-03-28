from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.assignment import Assignment
from schemas.assignment import AssignmentCreate, AssignmentResponse

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.post("/", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=list[AssignmentResponse])
def read_assignments(db: Session = Depends(get_db)):
    return db.query(Assignment).all()
