# System Architecture Documentation

## Overview

The AI-Powered Burnout Detection and Recovery Planning Agent is a full-stack web application designed to assess burnout levels and provide personalized recovery recommendations. The system follows a modular, service-oriented architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Assessment  │  │   Recovery   │  │   Progress   │      │
│  │    Form      │  │  Dashboard   │  │  Tracking    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │   Services   │  │   Models     │     │
│  │  (Endpoints) │  │  (Business   │  │  (Database)  │     │
│  │              │  │   Logic)     │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────┬───────────────────────────────┬───────────────┘
            │                               │
            ▼                               ▼
┌──────────────────────┐      ┌──────────────────────────┐
│   SQL Database      │      │   AI Service (LLM API)   │
│  (SQLite/PostgreSQL) │      │  - Google Gemini API     │
│  - Users             │      │  - Recovery Planning     │
│  - Assessments       │      │  - Ethical Constraints  │
│  - Recovery Plans    │      └──────────────────────────┘
│  - Progress          │
└──────────────────────┘
```

## Component Architecture

### Frontend Layer

**Technology Stack:**
- React 18.2+ (Functional components with hooks)
- React Router DOM for navigation
- Axios for HTTP requests
- Recharts for data visualization

**Key Components:**

1. **AssessmentForm.jsx**
   - Multi-step form for user registration and assessment
   - Client-side validation
   - Range sliders for intuitive input

2. **ResultPage.jsx**
   - Displays burnout score and classification
   - Visual breakdown of contributing factors
   - Triggers recovery plan generation

3. **RecoveryDashboard.jsx**
   - Displays AI-generated recovery plan
   - Interactive checklist for tracking actions
   - Plan regeneration capability

4. **ProgressTracking.jsx**
   - Historical score visualization
   - Trend analysis display
   - Manual progress record entry

### Backend Layer

**Technology Stack:**
- Python 3.8+
- FastAPI for RESTful API
- Raw SQL queries (SQLite for dev, PostgreSQL/Supabase for production)
- Pydantic for data validation

**Directory Structure:**

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Raw SQL database connection
│   ├── models.py            # Database schema definitions
│   ├── schemas.py           # Pydantic validation schemas
│   ├── schema.sql           # SQL schema (SQLite/PostgreSQL)
│   ├── schema_postgresql.sql # PostgreSQL-specific schema
│   ├── routes/              # API endpoint definitions
│   │   ├── users.py
│   │   ├── assessments.py
│   │   ├── recovery.py
│   │   └── progress.py
│   └── services/            # Business logic modules
│       ├── scoring.py       # Burnout scoring engine
│       ├── classification.py # Burnout classification
│       ├── ai_agent.py      # AI recovery planning
│       └── adaptive.py      # Adaptive follow-up logic
```

### Service Layer

#### 1. Scoring Engine (`services/scoring.py`)

**Purpose:** Convert questionnaire responses into numerical burnout scores (0-100).

**Algorithm:**
- Weighted factor analysis
- Normalization functions for each input type
- Aggregation with configurable weights

**Key Functions:**
- `calculate_score()`: Main scoring function
- Normalization helpers for each factor type

#### 2. Classification Module (`services/classification.py`)

**Purpose:** Classify burnout severity based on score thresholds.

**Classification Levels:**
- Healthy (0-25)
- Early Burnout (26-50)
- Moderate Burnout (51-75)
- Severe Burnout (76-100)

#### 3. AI Recovery Agent (`services/ai_agent.py`)

**Purpose:** Generate personalized recovery recommendations using LLM APIs.

**Features:**
- Ethical prompt engineering
- Structured JSON output validation
- Fallback recommendations if AI fails
- Uses Google Gemini API (free tier available)

**Ethical Constraints:**
- No medical diagnosis
- Supportive, non-judgmental language
- Professional help encouragement for severe cases

#### 4. Adaptive Follow-Up (`services/adaptive.py`)

**Purpose:** Analyze progress and adjust recovery plans dynamically.

**Logic:**
- Trend detection (improving, declining, stagnant)
- Score change analysis
- Automatic plan adjustment recommendations

### Database Layer

**Technology:** 
- SQLite (default for development) with raw SQL queries
- PostgreSQL/Supabase (for production) with raw SQL queries
- Automatic detection based on DATABASE_URL

**Schema:**

1. **Users Table**
   - Primary key: `user_id`
   - Fields: name, age_range, occupation_type, created_at

2. **Assessments Table**
   - Primary key: `assessment_id`
   - Foreign key: `user_id`
   - Fields: responses (JSON), burnout_score, burnout_stage, created_at

3. **RecoveryPlans Table**
   - Primary key: `plan_id`
   - Foreign key: `user_id`
   - Fields: recommendations (JSON), created_at, updated_at

4. **Progress Table**
   - Primary key: `progress_id`
   - Foreign key: `user_id`
   - Fields: weekly_score, completion_status (JSON), user_notes, timestamp

## Data Flow

### Assessment Flow

1. User fills assessment form (Frontend)
2. Form data sent to `/api/assessments/` (Backend)
3. Scoring engine calculates burnout score
4. Classification module determines stage
5. Assessment stored in database
6. Results returned to frontend
7. User views results on ResultPage

### Recovery Plan Generation Flow

1. User requests recovery plan (Frontend)
2. Request sent to `/api/recovery/generate` (Backend)
3. System retrieves latest assessment
4. Adaptive logic analyzes progress (if applicable)
5. Context built for AI agent
6. AI agent generates recommendations
7. Plan stored in database
8. Plan returned to frontend
9. User views plan on RecoveryDashboard

### Progress Tracking Flow

1. User views progress page (Frontend)
2. Request sent to `/api/progress/user/{id}/analysis` (Backend)
3. System retrieves assessment history
4. Adaptive logic analyzes trends
5. Chart data prepared from history
6. Analysis and chart data returned
7. User views progress visualization

## Security Considerations

1. **Input Validation:**
   - Pydantic schemas validate all inputs
   - Range checks on all numeric values
   - SQL injection protection via parameterized queries

2. **CORS Configuration:**
   - Restricted to frontend origin
   - Credentials allowed for session management

3. **Data Privacy:**
   - No storage of sensitive personal information
   - User data stored locally in browser (localStorage)
   - Database stored locally (SQLite) or in Supabase (PostgreSQL)

4. **API Security:**
   - Environment variables for API keys
   - No API keys exposed in frontend code
   - Parameterized SQL queries prevent injection attacks

## Scalability Considerations

**Current Implementation:**
- SQLite for development (single-server, file-based)
- PostgreSQL/Supabase support for production (scalable, cloud-hosted)
- Raw SQL queries for better performance and control
- No authentication/authorization (for demo purposes)
- Synchronous AI API calls

**Future Enhancements:**
- User authentication (JWT tokens)
- Async AI API calls
- Caching layer for frequently accessed data
- Background job processing for plan generation
- Connection pooling for PostgreSQL
- Read replicas for high-traffic scenarios

## Error Handling

1. **Frontend:**
   - Try-catch blocks around API calls
   - User-friendly error messages
   - Loading states for async operations

2. **Backend:**
   - HTTPException for API errors
   - Validation errors from Pydantic
   - Fallback recommendations if AI fails
   - Database transaction rollback on errors

## Testing Strategy

**Recommended Testing:**
- Unit tests for scoring engine
- Unit tests for classification logic
- Integration tests for API endpoints
- Frontend component tests
- End-to-end tests for user flows

## Deployment

**Development:**
- Frontend: `npm start` (port 3000)
- Backend: `uvicorn app.main:app --reload` (port 8000)

**Production:**
- Frontend: Build static files, serve with Nginx
- Backend: Deploy with Gunicorn/Uvicorn behind reverse proxy
- Database: Migrate to PostgreSQL for production
- Environment variables: Configure via .env or secrets management
