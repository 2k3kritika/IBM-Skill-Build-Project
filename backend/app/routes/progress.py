"""
Progress tracking routes using raw SQL.
"""
from fastapi import APIRouter, HTTPException
from app.database import execute_query, row_to_dict, dict_to_json
from app import schemas, models
from app.services.adaptive import AdaptiveFollowUp
import os

router = APIRouter(prefix="/api/progress", tags=["progress"])

IS_POSTGRES = os.getenv("DATABASE_URL", "").startswith(("postgresql://", "postgres://"))


@router.post("/", response_model=schemas.ProgressResponse, status_code=201)
def create_progress_record(progress: schemas.ProgressCreate):
    """
    Create a new progress record.
    """
    # Verify user exists
    user_query = "SELECT * FROM users WHERE user_id = " + ("%s" if IS_POSTGRES else "?")
    user = execute_query(user_query, params=(progress.user_id,), fetch_one=True)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create progress record
    completion_status_json = dict_to_json(progress.completion_status) if progress.completion_status else None
    
    if IS_POSTGRES:
        insert_query = """
            INSERT INTO progress (user_id, weekly_score, completion_status, user_notes, timestamp)
            VALUES (%s, %s, %s::jsonb, %s, CURRENT_TIMESTAMP)
            RETURNING progress_id, user_id, weekly_score, completion_status, user_notes, timestamp
        """
        result = execute_query(
            insert_query,
            params=(progress.user_id, progress.weekly_score, completion_status_json, progress.user_notes),
            fetch_one=True
        )
        return row_to_dict(result, json_fields=["completion_status"])
    else:
        insert_query = """
            INSERT INTO progress (user_id, weekly_score, completion_status, user_notes, timestamp)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        execute_query(
            insert_query,
            params=(progress.user_id, progress.weekly_score, completion_status_json, progress.user_notes)
        )
        
        # Get the inserted progress record
        get_query = "SELECT * FROM progress WHERE progress_id = (SELECT last_insert_rowid())"
        result = execute_query(get_query, fetch_one=True)
        return row_to_dict(result, json_fields=["completion_status"])


@router.get("/user/{user_id}", response_model=list[schemas.ProgressResponse])
def get_user_progress(user_id: int, skip: int = 0, limit: int = 20):
    """
    Get all progress records for a user, ordered by most recent first.
    """
    if IS_POSTGRES:
        query = """
            SELECT * FROM progress 
            WHERE user_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s OFFSET %s
        """
    else:
        query = """
            SELECT * FROM progress 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        """
    
    results = execute_query(query, params=(user_id, limit, skip), fetch_all=True)
    return [row_to_dict(row, json_fields=["completion_status"]) for row in results]


@router.get("/user/{user_id}/analysis")
def get_progress_analysis(user_id: int):
    """
    Get progress analysis including trend and recommendations.
    """
    # Get latest assessment
    if IS_POSTGRES:
        assessment_query = """
            SELECT * FROM assessments 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """
    else:
        assessment_query = """
            SELECT * FROM assessments 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        """
    
    latest_assessment = execute_query(assessment_query, params=(user_id,), fetch_one=True)
    
    if not latest_assessment:
        raise HTTPException(status_code=404, detail="No assessments found for user")
    
    assessment_dict = row_to_dict(latest_assessment, json_fields=["responses"])
    
    # Analyze progress
    adaptive = AdaptiveFollowUp()
    analysis = adaptive.analyze_progress(user_id, assessment_dict["burnout_score"])
    
    # Get progress history
    progress_history = adaptive.get_user_progress_history(user_id, limit=10)
    
    return {
        "current_score": assessment_dict["burnout_score"],
        "current_stage": assessment_dict["burnout_stage"],
        "progress_analysis": analysis,
        "progress_history": [
            {
                "progress_id": p["progress_id"],
                "weekly_score": p["weekly_score"],
                "timestamp": p["timestamp"],
                "user_notes": p.get("user_notes")
            }
            for p in progress_history
        ]
    }


@router.get("/{progress_id}", response_model=schemas.ProgressResponse)
def get_progress_record(progress_id: int):
    """
    Get progress record by ID.
    """
    query = "SELECT * FROM progress WHERE progress_id = " + ("%s" if IS_POSTGRES else "?")
    result = execute_query(query, params=(progress_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="Progress record not found")
    
    return row_to_dict(result, json_fields=["completion_status"])
