"""
Assessment routes for burnout evaluation using raw SQL.
"""
from fastapi import APIRouter, HTTPException
from app.database import execute_query, row_to_dict, dict_to_json
from app import schemas, models
from app.services.scoring import BurnoutScoringEngine
from app.services.classification import BurnoutClassifier
import os
import json

router = APIRouter(prefix="/api/assessments", tags=["assessments"])

IS_POSTGRES = os.getenv("DATABASE_URL", "").startswith(("postgresql://", "postgres://"))


@router.post("/", response_model=schemas.AssessmentResult, status_code=201)
def create_assessment(assessment: schemas.AssessmentCreate):
    """
    Create a new burnout assessment.
    Calculates score and classifies burnout stage.
    """
    # Verify user exists
    user_query = "SELECT * FROM users WHERE user_id = " + ("%s" if IS_POSTGRES else "?")
    user = execute_query(user_query, params=(assessment.user_id,), fetch_one=True)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate burnout score
    scoring_engine = BurnoutScoringEngine()
    score_result = scoring_engine.calculate_score(assessment.responses)
    
    # Classify burnout stage
    classifier = BurnoutClassifier()
    classification = classifier.classify(score_result["score"])
    
    # Store assessment
    responses_json = dict_to_json(assessment.responses.dict())
    
    if IS_POSTGRES:
        insert_query = """
            INSERT INTO assessments (user_id, responses, burnout_score, burnout_stage, created_at)
            VALUES (%s, %s::jsonb, %s, %s, CURRENT_TIMESTAMP)
            RETURNING assessment_id, user_id, burnout_score, burnout_stage, created_at
        """
        result = execute_query(
            insert_query,
            params=(assessment.user_id, responses_json, score_result["score"], classification["stage"]),
            fetch_one=True
        )
        return row_to_dict(result, json_fields=["responses"])
    else:
        insert_query = """
            INSERT INTO assessments (user_id, responses, burnout_score, burnout_stage, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        execute_query(
            insert_query,
            params=(assessment.user_id, responses_json, score_result["score"], classification["stage"])
        )
        
        # Get the inserted assessment
        get_query = "SELECT * FROM assessments WHERE assessment_id = (SELECT last_insert_rowid())"
        result = execute_query(get_query, fetch_one=True)
        return row_to_dict(result, json_fields=["responses"])


@router.get("/{assessment_id}", response_model=schemas.AssessmentResult)
def get_assessment(assessment_id: int):
    """
    Get assessment by ID.
    """
    query = "SELECT * FROM assessments WHERE assessment_id = " + ("%s" if IS_POSTGRES else "?")
    result = execute_query(query, params=(assessment_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return row_to_dict(result, json_fields=["responses"])


@router.get("/user/{user_id}", response_model=list[schemas.AssessmentResult])
def get_user_assessments(user_id: int, skip: int = 0, limit: int = 10):
    """
    Get all assessments for a user, ordered by most recent first.
    """
    if IS_POSTGRES:
        query = """
            SELECT * FROM assessments 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
    else:
        query = """
            SELECT * FROM assessments 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        """
    
    results = execute_query(query, params=(user_id, limit, skip), fetch_all=True)
    return [row_to_dict(row, json_fields=["responses"]) for row in results]


@router.get("/{assessment_id}/details")
def get_assessment_details(assessment_id: int):
    """
    Get detailed assessment information including score breakdown and classification.
    """
    query = "SELECT * FROM assessments WHERE assessment_id = " + ("%s" if IS_POSTGRES else "?")
    result = execute_query(query, params=(assessment_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    assessment = row_to_dict(result, json_fields=["responses"])
    
    # Recalculate to get breakdown
    scoring_engine = BurnoutScoringEngine()
    responses = schemas.AssessmentResponse(**assessment["responses"])
    score_result = scoring_engine.calculate_score(responses)
    
    classifier = BurnoutClassifier()
    classification = classifier.classify(assessment["burnout_score"])
    
    return {
        "assessment_id": assessment["assessment_id"],
        "user_id": assessment["user_id"],
        "burnout_score": assessment["burnout_score"],
        "burnout_stage": assessment["burnout_stage"],
        "score_breakdown": score_result["breakdown"],
        "explanation": score_result["explanation"],
        "classification": classification,
        "created_at": assessment["created_at"]
    }
