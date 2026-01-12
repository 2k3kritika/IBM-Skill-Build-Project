"""
Burnout scoring engine.
Converts questionnaire responses into a numerical burnout score (0-100).
"""
from typing import Dict, Any
from app.schemas import AssessmentResponse


class BurnoutScoringEngine:
    """
    Calculates burnout score based on weighted factors.
    """
    
    # Weight factors for each component
    WEIGHTS = {
        "work_hours": 0.15,      # Daily work hours (normalized)
        "sleep_duration": 0.10,   # Sleep duration (normalized)
        "sleep_quality": 0.15,    # Sleep quality (inverted: low quality = high burnout)
        "emotional_exhaustion": 0.25,  # High weight for emotional exhaustion
        "motivation": 0.15,       # Motivation (inverted: low motivation = high burnout)
        "screen_time": 0.10,      # Screen time (normalized)
        "perceived_stress": 0.10  # Perceived stress
    }

    @staticmethod
    def normalize_work_hours(hours: float) -> float:
        """
        Normalize work hours to 0-1 scale.
        Assumes 8 hours is normal, >12 hours is high stress.
        """
        if hours <= 8:
            return 0.0
        elif hours >= 12:
            return 1.0
        else:
            return (hours - 8) / 4.0

    @staticmethod
    def normalize_sleep_duration(hours: float) -> float:
        """
        Normalize sleep duration to 0-1 scale.
        Assumes 7-9 hours is optimal, <6 or >10 is problematic.
        """
        if 7 <= hours <= 9:
            return 0.0
        elif hours < 6:
            return 1.0 - (hours / 6.0)  # Less sleep = higher burnout
        elif hours > 10:
            return (hours - 10) / 4.0  # Too much sleep can indicate issues
        else:
            return abs(hours - 8) / 2.0

    @staticmethod
    def normalize_sleep_quality(quality: int) -> float:
        """
        Invert sleep quality (1-5 scale) to burnout contribution.
        Low quality (1-2) = high burnout, high quality (4-5) = low burnout.
        """
        return (6 - quality) / 5.0  # Invert: 1->1.0, 5->0.2

    @staticmethod
    def normalize_emotional_exhaustion(level: int) -> float:
        """
        Convert emotional exhaustion (1-5) to 0-1 scale.
        """
        return (level - 1) / 4.0

    @staticmethod
    def normalize_motivation(level: int) -> float:
        """
        Invert motivation (1-5) to burnout contribution.
        Low motivation = high burnout.
        """
        return (6 - level) / 5.0

    @staticmethod
    def normalize_screen_time(hours: float) -> float:
        """
        Normalize screen time to 0-1 scale.
        Assumes >8 hours is high, <4 hours is low.
        """
        if hours <= 4:
            return 0.0
        elif hours >= 12:
            return 1.0
        else:
            return (hours - 4) / 8.0

    @staticmethod
    def normalize_stress(level: int) -> float:
        """
        Convert perceived stress (1-5) to 0-1 scale.
        """
        return (level - 1) / 4.0

    @classmethod
    def calculate_score(cls, responses: AssessmentResponse) -> Dict[str, Any]:
        """
        Calculate burnout score from assessment responses.
        
        Returns:
            Dict containing:
                - score: float (0-100)
                - breakdown: dict with component contributions
                - explanation: str describing the score
        """
        # Normalize all components
        work_contrib = cls.normalize_work_hours(responses.daily_work_hours) * cls.WEIGHTS["work_hours"]
        sleep_dur_contrib = cls.normalize_sleep_duration(responses.sleep_duration) * cls.WEIGHTS["sleep_duration"]
        sleep_qual_contrib = cls.normalize_sleep_quality(responses.sleep_quality) * cls.WEIGHTS["sleep_quality"]
        emotional_contrib = cls.normalize_emotional_exhaustion(responses.emotional_exhaustion) * cls.WEIGHTS["emotional_exhaustion"]
        motivation_contrib = cls.normalize_motivation(responses.motivation_level) * cls.WEIGHTS["motivation"]
        screen_contrib = cls.normalize_screen_time(responses.screen_time) * cls.WEIGHTS["screen_time"]
        stress_contrib = cls.normalize_stress(responses.perceived_stress) * cls.WEIGHTS["perceived_stress"]

        # Calculate total score (0-1 scale, then convert to 0-100)
        total_normalized = (
            work_contrib +
            sleep_dur_contrib +
            sleep_qual_contrib +
            emotional_contrib +
            motivation_contrib +
            screen_contrib +
            stress_contrib
        )

        # Ensure score is between 0 and 100
        score = min(100, max(0, total_normalized * 100))

        # Create breakdown for transparency
        breakdown = {
            "work_hours": round(work_contrib * 100, 2),
            "sleep_duration": round(sleep_dur_contrib * 100, 2),
            "sleep_quality": round(sleep_qual_contrib * 100, 2),
            "emotional_exhaustion": round(emotional_contrib * 100, 2),
            "motivation": round(motivation_contrib * 100, 2),
            "screen_time": round(screen_contrib * 100, 2),
            "perceived_stress": round(stress_contrib * 100, 2)
        }

        # Generate explanation
        top_factors = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
        explanation = f"Your burnout score is {score:.1f}/100. "
        explanation += "Primary contributing factors: "
        explanation += ", ".join([f"{factor} ({value:.1f}%)" for factor, value in top_factors])

        return {
            "score": round(score, 2),
            "breakdown": breakdown,
            "explanation": explanation
        }
