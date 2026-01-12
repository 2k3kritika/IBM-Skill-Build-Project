"""
AI Recovery Planning Agent.
Generates personalized recovery recommendations using Google Gemini API.
"""
import os
import json
from typing import Dict, Any, Optional
from app.schemas import RecoveryRecommendations, AssessmentResponse
from dotenv import load_dotenv

load_dotenv()


class AIRecoveryAgent:
    """
    AI agent for generating personalized recovery plans.
    Uses Google Gemini API (free tier available).
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

    def _get_gemini_client(self):
        """Get Google Gemini client."""
        try:
            import google.generativeai as genai
            if not self.gemini_api_key:
                raise ValueError("GOOGLE_GEMINI_API_KEY not set")
            genai.configure(api_key=self.gemini_api_key)
            return genai.GenerativeModel(self.model_name)
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")

    def _build_prompt(self, burnout_context: Dict[str, Any]) -> str:
        """
        Build ethical, structured prompt for AI agent.
        
        Args:
            burnout_context: Dict containing score, stage, responses, etc.
            
        Returns:
            Formatted prompt string
        """
        score = burnout_context.get("score", 0)
        stage = burnout_context.get("stage", "Unknown")
        responses = burnout_context.get("responses", {})
        
        prompt = f"""You are a supportive wellness assistant helping someone with burnout recovery planning.

CONTEXT:
- Burnout Score: {score}/100
- Burnout Stage: {stage}
- Daily work hours: {responses.get('daily_work_hours', 'N/A')} hours
- Sleep duration: {responses.get('sleep_duration', 'N/A')} hours
- Sleep quality: {responses.get('sleep_quality', 'N/A')}/5
- Emotional exhaustion: {responses.get('emotional_exhaustion', 'N/A')}/5
- Motivation level: {responses.get('motivation_level', 'N/A')}/5
- Screen time: {responses.get('screen_time', 'N/A')} hours/day
- Perceived stress: {responses.get('perceived_stress', 'N/A')}/5

CRITICAL ETHICAL CONSTRAINTS:
1. DO NOT provide medical diagnosis or treatment advice
2. DO NOT use alarming or judgmental language
3. DO use supportive, empathetic, and neutral tone
4. DO encourage professional help if burnout is severe (score > 75)
5. DO focus on lifestyle adjustments, self-care, and stress management
6. DO provide actionable, realistic recommendations

TASK:
Generate a personalized recovery plan in the following JSON format:
{{
    "daily_actions": ["action 1", "action 2", "action 3"],
    "weekly_goals": ["goal 1", "goal 2", "goal 3"],
    "behavioral_suggestions": ["suggestion 1", "suggestion 2"],
    "caution_notes": ["note 1", "note 2"],
    "disclaimer": "This is not medical advice. Please consult a healthcare professional for severe symptoms."
}}

REQUIREMENTS:
- Provide 3-5 daily actions (small, achievable micro-actions)
- Provide 2-3 weekly goals (broader recovery objectives)
- Provide 2-4 behavioral suggestions (lifestyle adjustments)
- Include caution notes if score > 75 (encouraging professional consultation)
- All recommendations must be practical and non-medical
- Tailor recommendations to the specific burnout context provided

Respond ONLY with valid JSON, no additional text."""

        return prompt

    def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        """Call Google Gemini API."""
        model = self._get_gemini_client()
        content = ""
        
        try:
            # Build the full prompt with system instructions
            full_prompt = f"""You are a supportive wellness assistant. Always respond with valid JSON only.

{prompt}"""
            
            # Generate content using Gemini
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1000,
                }
            )
            
            content = response.text.strip()
            
            # Try to parse JSON (handle markdown code blocks if present)
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse Gemini JSON response: {str(e)}"
            if content:
                error_msg += f". Response: {content[:200]}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def generate_recovery_plan(self, burnout_context: Dict[str, Any]) -> RecoveryRecommendations:
        """
        Generate personalized recovery plan using AI.
        
        Args:
            burnout_context: Dict containing:
                - score: float
                - stage: str
                - stage_key: str
                - responses: dict (assessment responses)
                - description: str
                
        Returns:
            RecoveryRecommendations object
        """
        prompt = self._build_prompt(burnout_context)
        
        try:
            ai_response = self._call_gemini(prompt)
            
            # Validate and structure response
            recommendations = RecoveryRecommendations(
                daily_actions=ai_response.get("daily_actions", []),
                weekly_goals=ai_response.get("weekly_goals", []),
                behavioral_suggestions=ai_response.get("behavioral_suggestions", []),
                caution_notes=ai_response.get("caution_notes", []),
                disclaimer=ai_response.get("disclaimer", "This is not medical advice.")
            )
            
            return recommendations
            
        except Exception as e:
            # Fallback to default recommendations if AI fails
            return self._get_fallback_recommendations(burnout_context)

    def _get_fallback_recommendations(self, burnout_context: Dict[str, Any]) -> RecoveryRecommendations:
        """
        Provide fallback recommendations if AI fails.
        """
        score = burnout_context.get("score", 50)
        stage_key = burnout_context.get("stage_key", "early_burnout")
        
        if stage_key == "severe_burnout":
            daily_actions = [
                "Take 10-minute breaks every 2 hours",
                "Practice deep breathing exercises 3 times daily",
                "Ensure 7-8 hours of sleep"
            ]
            weekly_goals = [
                "Reduce work hours by 10% if possible",
                "Schedule one day completely off from work"
            ]
            behavioral_suggestions = [
                "Consider consulting a healthcare professional",
                "Establish clear work boundaries",
                "Prioritize rest and recovery"
            ]
            caution_notes = [
                "Severe burnout may require professional intervention",
                "Monitor symptoms and seek help if they worsen"
            ]
        elif stage_key == "moderate_burnout":
            daily_actions = [
                "Take regular breaks during work",
                "Practice mindfulness for 10 minutes",
                "Maintain consistent sleep schedule"
            ]
            weekly_goals = [
                "Implement work-life boundaries",
                "Engage in one enjoyable activity"
            ]
            behavioral_suggestions = [
                "Review and adjust work commitments",
                "Increase physical activity gradually"
            ]
            caution_notes = []
        else:
            daily_actions = [
                "Maintain current healthy habits",
                "Continue stress management practices"
            ]
            weekly_goals = [
                "Monitor stress levels regularly"
            ]
            behavioral_suggestions = [
                "Prevent burnout through proactive self-care"
            ]
            caution_notes = []
        
        return RecoveryRecommendations(
            daily_actions=daily_actions,
            weekly_goals=weekly_goals,
            behavioral_suggestions=behavioral_suggestions,
            caution_notes=caution_notes,
            disclaimer="This is not medical advice. Please consult a healthcare professional for severe symptoms."
        )
