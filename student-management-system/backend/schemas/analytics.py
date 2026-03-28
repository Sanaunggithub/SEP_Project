from pydantic import BaseModel

class AnalyticsBase(BaseModel):
    metric: str
    value: float

class AnalyticsCreate(AnalyticsBase):
    pass

class AnalyticsResponse(AnalyticsBase):
    id: int

    class Config:
        orm_mode = True
