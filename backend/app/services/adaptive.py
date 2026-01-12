"""
Adaptive follow-up logic using raw SQL.
Compares current and previous burnout scores to adjust recovery plans.
"""
from typing import Dict, Any, List
from app.database import execute_query, row_to_dict
import os

IS_POSTGRES = os.getenv("DATABASE_URL", "").startswith(("postgresql://", "postgres://"))


class AdaptiveFollowUp:
    """
    Adaptive logic for adjusting recovery plans based on progress.
    """
    
    IMPROVEMENT_THRESHOLD = 5.0  # Points improvement considered significant
    REGRESSION_THRESHOLD = 5.0   # Points decline considered regression
    STAGNATION_WEEKS = 2          # Weeks without improvement before adjustment

    @staticmethod
    def get_user_assessment_history(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's assessment history, ordered by most recent first.
        """
        if IS_POSTGRES:
            query = """
                SELECT * FROM assessments 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """
        else:
            query = """
                SELECT * FROM assessments 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """
        
        results = execute_query(query, params=(user_id, limit), fetch_all=True)
        return [row_to_dict(row, json_fields=["responses"]) for row in results]

    @staticmethod
    def get_user_progress_history(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's progress history, ordered by most recent first.
        """
        if IS_POSTGRES:
            query = """
                SELECT * FROM progress 
                WHERE user_id = %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            """
        else:
            query = """
                SELECT * FROM progress 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
        
        results = execute_query(query, params=(user_id, limit), fetch_all=True)
        return [row_to_dict(row, json_fields=["completion_status"]) for row in results]

    @classmethod
    def analyze_progress(cls, user_id: int, current_score: float) -> Dict[str, Any]:
        """
        Analyze user's progress and determine if recovery plan needs adjustment.
        
        Args:
            user_id: User ID
            current_score: Current burnout score
            
        Returns:
            Dict containing:
                - trend: str (improving, declining, stagnant)
                - change: float (score change from previous)
                - recommendation: str (adjustment recommendation)
                - needs_adjustment: bool
        """
        assessments = cls.get_user_assessment_history(user_id, limit=5)
        
        if len(assessments) < 2:
            return {
                "trend": "insufficient_data",
                "change": 0.0,
                "recommendation": "Continue with current plan. More data needed for trend analysis.",
                "needs_adjustment": False
            }
        
        previous_score = assessments[1]["burnout_score"]  # Second most recent
        change = current_score - previous_score
        
        if change <= -cls.IMPROVEMENT_THRESHOLD:
            trend = "improving"
            recommendation = (
                "Great progress! Your burnout score has improved. "
                "Continue with current recovery plan and consider maintaining these positive changes."
            )
            needs_adjustment = False
        elif change >= cls.REGRESSION_THRESHOLD:
            trend = "declining"
            recommendation = (
                "Your burnout score has increased. This may indicate increased stress or challenges. "
                "Consider intensifying recovery efforts or consulting a healthcare professional if symptoms persist."
            )
            needs_adjustment = True
        else:
            # Check for stagnation over multiple weeks
            if len(assessments) >= cls.STAGNATION_WEEKS + 1:
                recent_scores = [a["burnout_score"] for a in assessments[:cls.STAGNATION_WEEKS + 1]]
                if all(abs(s - recent_scores[0]) < cls.IMPROVEMENT_THRESHOLD for s in recent_scores):
                    trend = "stagnant"
                    recommendation = (
                        "Your burnout score has remained relatively stable. "
                        "Consider trying different recovery strategies or increasing intervention intensity."
                    )
                    needs_adjustment = True
                else:
                    trend = "stable"
                    recommendation = "Your score is relatively stable. Continue monitoring and maintaining current efforts."
                    needs_adjustment = False
            else:
                trend = "stable"
                recommendation = "Continue monitoring your progress. More time is needed to assess trends."
                needs_adjustment = False
        
        return {
            "trend": trend,
            "change": round(change, 2),
            "recommendation": recommendation,
            "needs_adjustment": needs_adjustment,
            "previous_score": previous_score,
            "current_score": current_score
        }

    @classmethod
    def generate_adjusted_plan_context(cls, progress_analysis: Dict[str, Any], 
                                       original_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate context for creating an adjusted recovery plan.
        
        Args:
            progress_analysis: Output from analyze_progress
            original_context: Original burnout context
            
        Returns:
            Updated context dict for AI agent
        """
        adjusted_context = original_context.copy()
        adjusted_context["progress_trend"] = progress_analysis["trend"]
        adjusted_context["score_change"] = progress_analysis["change"]
        adjusted_context["adjustment_needed"] = progress_analysis["needs_adjustment"]
        adjusted_context["progress_recommendation"] = progress_analysis["recommendation"]
        
        return adjusted_context
