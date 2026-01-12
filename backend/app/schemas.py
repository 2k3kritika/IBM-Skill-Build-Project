"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age_range: str = Field(..., pattern="^(18-25|26-35|36-45|46-55|56-65|65\\+)$")
    occupation_type: str = Field(..., pattern="^(student|professional|other)$")


class UserResponse(BaseModel):
    user_id: int
    name: str
    age_range: str
    occupation_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# Assessment Schemas
class AssessmentResponse(BaseModel):
    """
    Schema for assessment questionnaire responses.
    All values should be on a scale of 1-5.
    """
    daily_work_hours: float = Field(..., ge=0, le=24, description="Daily work/study hours")
    sleep_duration: float = Field(..., ge=0, le=24, description="Sleep duration in hours")
    sleep_quality: int = Field(..., ge=1, le=5, description="Sleep quality (1=poor, 5=excellent)")
    emotional_exhaustion: int = Field(..., ge=1, le=5, description="Emotional exhaustion level (1=low, 5=high)")
    motivation_level: int = Field(..., ge=1, le=5, description="Motivation and engagement (1=low, 5=high)")
    screen_time: float = Field(..., ge=0, le=24, description="Screen time per day in hours")
    perceived_stress: int = Field(..., ge=1, le=5, description="Perceived stress level (1=low, 5=high)")

    @field_validator('daily_work_hours', 'sleep_duration', 'screen_time')
    @classmethod
    def validate_hours(cls, v):
        if v > 24:
            raise ValueError("Hours cannot exceed 24")
        return v


class AssessmentResult(BaseModel):
    assessment_id: int
    user_id: int
    burnout_score: float = Field(..., ge=0, le=100)
    burnout_stage: str
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentCreate(BaseModel):
    user_id: int
    responses: AssessmentResponse


# Recovery Plan Schemas
class RecoveryPlanResponse(BaseModel):
    plan_id: int
    user_id: int
    recommendations: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecoveryPlanCreate(BaseModel):
    user_id: int
    assessment_id: int


# Progress Schemas
class ProgressCreate(BaseModel):
    user_id: int
    weekly_score: float = Field(..., ge=0, le=100)
    completion_status: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None


class ProgressResponse(BaseModel):
    progress_id: int
    user_id: int
    weekly_score: float
    completion_status: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


# AI Agent Schemas
class RecoveryRecommendations(BaseModel):
    """
    Structured format for AI-generated recovery recommendations.
    """
    daily_actions: List[str]
    weekly_goals: List[str]
    behavioral_suggestions: List[str]
    caution_notes: List[str]
    disclaimer: str = "This is not medical advice. Please consult a healthcare professional for severe symptoms."
