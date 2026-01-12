"""
Database schema definitions and table names.
This file contains table names and field definitions for reference.
Actual database structure is defined in schema.sql.
"""

# Table names
USERS_TABLE = "users"
ASSESSMENTS_TABLE = "assessments"
RECOVERY_PLANS_TABLE = "recovery_plans"
PROGRESS_TABLE = "progress"

# Field names for reference
USER_FIELDS = ["user_id", "name", "age_range", "occupation_type", "created_at"]
ASSESSMENT_FIELDS = ["assessment_id", "user_id", "responses", "burnout_score", "burnout_stage", "created_at"]
RECOVERY_PLAN_FIELDS = ["plan_id", "user_id", "recommendations", "created_at", "updated_at"]
PROGRESS_FIELDS = ["progress_id", "user_id", "weekly_score", "completion_status", "user_notes", "timestamp"]

# JSON fields that need conversion
JSON_FIELDS = {
    ASSESSMENTS_TABLE: ["responses"],
    RECOVERY_PLANS_TABLE: ["recommendations"],
    PROGRESS_TABLE: ["completion_status"]
}
