-- Database schema for AI-Powered Burnout Detection and Recovery Planning Agent
-- Supports both SQLite and PostgreSQL (Supabase)

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PostgreSQL: SERIAL PRIMARY KEY
    name VARCHAR(100) NOT NULL,
    age_range VARCHAR(20) NOT NULL,
    occupation_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assessments table
CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PostgreSQL: SERIAL PRIMARY KEY
    user_id INTEGER NOT NULL,
    responses TEXT NOT NULL,  -- JSON stored as TEXT
    burnout_score REAL NOT NULL,
    burnout_stage VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Recovery plans table
CREATE TABLE IF NOT EXISTS recovery_plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PostgreSQL: SERIAL PRIMARY KEY
    user_id INTEGER NOT NULL,
    recommendations TEXT NOT NULL,  -- JSON stored as TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Progress table
CREATE TABLE IF NOT EXISTS progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PostgreSQL: SERIAL PRIMARY KEY
    user_id INTEGER NOT NULL,
    weekly_score REAL NOT NULL,
    completion_status TEXT,  -- JSON stored as TEXT (nullable)
    user_notes TEXT,  -- Nullable
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_assessments_user_id ON assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_assessments_created_at ON assessments(created_at);
CREATE INDEX IF NOT EXISTS idx_recovery_plans_user_id ON recovery_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_recovery_plans_created_at ON recovery_plans(created_at);
CREATE INDEX IF NOT EXISTS idx_progress_user_id ON progress(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_timestamp ON progress(timestamp);
