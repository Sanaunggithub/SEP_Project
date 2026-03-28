from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.analytics import Analytics
from schemas.analytics import AnalyticsCreate, AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/", response_model=AnalyticsResponse)
def create_analytics(analytics: AnalyticsCreate, db: Session = Depends(get_db)):
    db_analytics = Analytics(**analytics.dict())
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics

@router.get("/", response_model=list[AnalyticsResponse])
def read_analytics(db: Session = Depends(get_db)):
    return db.query(Analytics).all()
