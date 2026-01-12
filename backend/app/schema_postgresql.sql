-- PostgreSQL-specific schema for Supabase
-- Use this when migrating to Supabase/PostgreSQL

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age_range VARCHAR(20) NOT NULL,
    occupation_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Assessments table
CREATE TABLE IF NOT EXISTS assessments (
    assessment_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    responses JSONB NOT NULL,  -- PostgreSQL JSONB for better performance
    burnout_score REAL NOT NULL,
    burnout_stage VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Recovery plans table
CREATE TABLE IF NOT EXISTS recovery_plans (
    plan_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    recommendations JSONB NOT NULL,  -- PostgreSQL JSONB
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Progress table
CREATE TABLE IF NOT EXISTS progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    weekly_score REAL NOT NULL,
    completion_status JSONB,  -- PostgreSQL JSONB (nullable)
    user_notes TEXT,  -- Nullable
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_assessments_user_id ON assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_assessments_created_at ON assessments(created_at);
CREATE INDEX IF NOT EXISTS idx_recovery_plans_user_id ON recovery_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_recovery_plans_created_at ON recovery_plans(created_at);
CREATE INDEX IF NOT EXISTS idx_progress_user_id ON progress(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_timestamp ON progress(timestamp);

-- For Supabase: Enable Row Level Security (RLS) if needed
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE recovery_plans ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE progress ENABLE ROW LEVEL SECURITY;
