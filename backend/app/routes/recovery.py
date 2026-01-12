"""
Recovery plan routes using raw SQL.
"""
from fastapi import APIRouter, HTTPException
from app.database import execute_query, row_to_dict, dict_to_json
from app import schemas, models
from app.services.ai_agent import AIRecoveryAgent
from app.services.adaptive import AdaptiveFollowUp
from app.services.classification import BurnoutClassifier
import os

router = APIRouter(prefix="/api/recovery", tags=["recovery"])

IS_POSTGRES = os.getenv("DATABASE_URL", "").startswith(("postgresql://", "postgres://"))


@router.post("/generate", response_model=schemas.RecoveryPlanResponse, status_code=201)
def generate_recovery_plan(plan_request: schemas.RecoveryPlanCreate):
    """
    Generate a new AI-powered recovery plan based on assessment.
    """
    # Verify user exists
    user_query = "SELECT * FROM users WHERE user_id = " + ("%s" if IS_POSTGRES else "?")
    user = execute_query(user_query, params=(plan_request.user_id,), fetch_one=True)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get assessment
    assessment_query = "SELECT * FROM assessments WHERE assessment_id = " + ("%s" if IS_POSTGRES else "?")
    assessment = execute_query(assessment_query, params=(plan_request.assessment_id,), fetch_one=True)
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    assessment_dict = row_to_dict(assessment, json_fields=["responses"])
    
    if assessment_dict["user_id"] != plan_request.user_id:
        raise HTTPException(status_code=400, detail="Assessment does not belong to user")
    
    # Get classification details
    classifier = BurnoutClassifier()
    classification = classifier.classify(assessment_dict["burnout_score"])
    
    # Build context for AI agent
    burnout_context = {
        "score": assessment_dict["burnout_score"],
        "stage": assessment_dict["burnout_stage"],
        "stage_key": classification["stage_key"],
        "responses": assessment_dict["responses"],
        "description": classification["description"]
    }
    
    # Check for progress and adapt if needed
    adaptive = AdaptiveFollowUp()
    progress_analysis = adaptive.analyze_progress(plan_request.user_id, assessment_dict["burnout_score"])
    
    if progress_analysis["needs_adjustment"]:
        burnout_context = adaptive.generate_adjusted_plan_context(progress_analysis, burnout_context)
    
    # Generate recovery plan using AI
    ai_agent = AIRecoveryAgent()
    recommendations = ai_agent.generate_recovery_plan(burnout_context)
    
    # Store recovery plan
    recommendations_json = dict_to_json(recommendations.dict())
    
    if IS_POSTGRES:
        insert_query = """
            INSERT INTO recovery_plans (user_id, recommendations, created_at)
            VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
            RETURNING plan_id, user_id, recommendations, created_at, updated_at
        """
        result = execute_query(
            insert_query,
            params=(plan_request.user_id, recommendations_json),
            fetch_one=True
        )
        return row_to_dict(result, json_fields=["recommendations"])
    else:
        insert_query = """
            INSERT INTO recovery_plans (user_id, recommendations, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """
        execute_query(insert_query, params=(plan_request.user_id, recommendations_json))
        
        # Get the inserted plan
        get_query = "SELECT * FROM recovery_plans WHERE plan_id = (SELECT last_insert_rowid())"
        result = execute_query(get_query, fetch_one=True)
        return row_to_dict(result, json_fields=["recommendations"])


@router.get("/user/{user_id}/latest", response_model=schemas.RecoveryPlanResponse)
def get_latest_recovery_plan(user_id: int):
    """
    Get the most recent recovery plan for a user.
    """
    if IS_POSTGRES:
        query = """
            SELECT * FROM recovery_plans 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """
    else:
        query = """
            SELECT * FROM recovery_plans 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        """
    
    result = execute_query(query, params=(user_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="No recovery plan found for user")
    
    return row_to_dict(result, json_fields=["recommendations"])


@router.get("/{plan_id}", response_model=schemas.RecoveryPlanResponse)
def get_recovery_plan(plan_id: int):
    """
    Get recovery plan by ID.
    """
    query = "SELECT * FROM recovery_plans WHERE plan_id = " + ("%s" if IS_POSTGRES else "?")
    result = execute_query(query, params=(plan_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="Recovery plan not found")
    
    return row_to_dict(result, json_fields=["recommendations"])


@router.post("/{plan_id}/regenerate")
def regenerate_recovery_plan(plan_id: int):
    """
    Regenerate a recovery plan (useful for adaptive updates).
    """
    plan_query = "SELECT * FROM recovery_plans WHERE plan_id = " + ("%s" if IS_POSTGRES else "?")
    plan = execute_query(plan_query, params=(plan_id,), fetch_one=True)
    
    if not plan:
        raise HTTPException(status_code=404, detail="Recovery plan not found")
    
    plan_dict = row_to_dict(plan, json_fields=["recommendations"])
    
    # Get latest assessment for user
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
    
    assessment = execute_query(assessment_query, params=(plan_dict["user_id"],), fetch_one=True)
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for user")
    
    assessment_dict = row_to_dict(assessment, json_fields=["responses"])
    
    # Regenerate with adaptive logic
    classifier = BurnoutClassifier()
    classification = classifier.classify(assessment_dict["burnout_score"])
    
    burnout_context = {
        "score": assessment_dict["burnout_score"],
        "stage": assessment_dict["burnout_stage"],
        "stage_key": classification["stage_key"],
        "responses": assessment_dict["responses"],
        "description": classification["description"]
    }
    
    adaptive = AdaptiveFollowUp()
    progress_analysis = adaptive.analyze_progress(plan_dict["user_id"], assessment_dict["burnout_score"])
    
    if progress_analysis["needs_adjustment"]:
        burnout_context = adaptive.generate_adjusted_plan_context(progress_analysis, burnout_context)
    
    ai_agent = AIRecoveryAgent()
    recommendations = ai_agent.generate_recovery_plan(burnout_context)
    
    # Update existing plan
    recommendations_json = dict_to_json(recommendations.dict())
    
    if IS_POSTGRES:
        update_query = """
            UPDATE recovery_plans 
            SET recommendations = %s::jsonb, updated_at = CURRENT_TIMESTAMP
            WHERE plan_id = %s
            RETURNING plan_id, user_id, recommendations, created_at, updated_at
        """
        result = execute_query(
            update_query,
            params=(recommendations_json, plan_id),
            fetch_one=True
        )
        return row_to_dict(result, json_fields=["recommendations"])
    else:
        update_query = """
            UPDATE recovery_plans 
            SET recommendations = ?, updated_at = CURRENT_TIMESTAMP
            WHERE plan_id = ?
        """
        execute_query(update_query, params=(recommendations_json, plan_id))
        
        # Get updated plan
        get_query = "SELECT * FROM recovery_plans WHERE plan_id = " + ("%s" if IS_POSTGRES else "?")
        result = execute_query(get_query, params=(plan_id,), fetch_one=True)
        return row_to_dict(result, json_fields=["recommendations"])
