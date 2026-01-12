"""
Burnout classification module.
Classifies burnout severity based on score thresholds.
"""
from typing import Dict, Any


class BurnoutClassifier:
    """
    Classifies burnout stage based on score.
    """
    
    # Threshold definitions
    THRESHOLDS = {
        "healthy": (0, 25),
        "early_burnout": (26, 50),
        "moderate_burnout": (51, 75),
        "severe_burnout": (76, 100)
    }

    @classmethod
    def classify(cls, score: float) -> Dict[str, Any]:
        """
        Classify burnout stage based on score.
        
        Args:
            score: Burnout score (0-100)
            
        Returns:
            Dict containing:
                - stage: str (Healthy, Early Burnout, Moderate Burnout, Severe Burnout)
                - stage_key: str (internal key)
                - description: str (explanation of the stage)
                - recommendations_level: str (suggested intervention level)
        """
        score = max(0, min(100, score))  # Clamp to 0-100
        
        if score <= 25:
            stage_key = "healthy"
            stage = "Healthy"
            description = (
                "Your assessment indicates a healthy balance. You're managing stress well "
                "and maintaining good work-life boundaries. Continue practicing self-care."
            )
            recommendations_level = "maintenance"
        elif score <= 50:
            stage_key = "early_burnout"
            stage = "Early Burnout"
            description = (
                "You're showing early signs of burnout. This is a good time to take proactive steps "
                "to prevent further progression. Focus on stress management and work-life balance."
            )
            recommendations_level = "preventive"
        elif score <= 75:
            stage_key = "moderate_burnout"
            stage = "Moderate Burnout"
            description = (
                "You're experiencing moderate burnout symptoms. It's important to take action now "
                "to prevent escalation. Consider lifestyle adjustments and stress reduction techniques. "
                "If symptoms persist, consider consulting a healthcare professional."
            )
            recommendations_level = "intervention"
        else:
            stage_key = "severe_burnout"
            stage = "Severe Burnout"
            description = (
                "Your assessment indicates severe burnout levels. This requires immediate attention. "
                "Please consider consulting with a healthcare professional or mental health specialist. "
                "The recommendations provided are supportive measures and should not replace professional care."
            )
            recommendations_level = "urgent"

        return {
            "stage": stage,
            "stage_key": stage_key,
            "description": description,
            "recommendations_level": recommendations_level,
            "score_range": cls.THRESHOLDS[stage_key]
        }
