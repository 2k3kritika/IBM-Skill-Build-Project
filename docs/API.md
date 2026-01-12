# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication. User identification is handled via `user_id` in requests.

## Endpoints

### Users

#### Create User

**POST** `/users/`

Create a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "age_range": "26-35",
  "occupation_type": "professional"
}
```

**Response:** `201 Created`
```json
{
  "user_id": 1,
  "name": "John Doe",
  "age_range": "26-35",
  "occupation_type": "professional",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Validation:**
- `age_range`: Must be one of: "18-25", "26-35", "36-45", "46-55", "56-65", "65+"
- `occupation_type`: Must be one of: "student", "professional", "other"

---

#### Get User

**GET** `/users/{user_id}`

Get user by ID.

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "name": "John Doe",
  "age_range": "26-35",
  "occupation_type": "professional",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error:** `404 Not Found` if user doesn't exist.

---

#### List Users

**GET** `/users/?skip=0&limit=100`

List all users (for testing/admin purposes).

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "user_id": 1,
    "name": "John Doe",
    ...
  }
]
```

---

### Assessments

#### Create Assessment

**POST** `/assessments/`

Create a new burnout assessment.

**Request Body:**
```json
{
  "user_id": 1,
  "responses": {
    "daily_work_hours": 10.0,
    "sleep_duration": 6.5,
    "sleep_quality": 2,
    "emotional_exhaustion": 4,
    "motivation_level": 2,
    "screen_time": 10.0,
    "perceived_stress": 4
  }
}
```

**Response:** `201 Created`
```json
{
  "assessment_id": 1,
  "user_id": 1,
  "burnout_score": 68.5,
  "burnout_stage": "Moderate Burnout",
  "created_at": "2024-01-15T10:35:00Z"
}
```

**Validation:**
- `daily_work_hours`: 0-24
- `sleep_duration`: 0-24
- `sleep_quality`: 1-5
- `emotional_exhaustion`: 1-5
- `motivation_level`: 1-5
- `screen_time`: 0-24
- `perceived_stress`: 1-5

---

#### Get Assessment

**GET** `/assessments/{assessment_id}`

Get assessment by ID.

**Response:** `200 OK`
```json
{
  "assessment_id": 1,
  "user_id": 1,
  "burnout_score": 68.5,
  "burnout_stage": "Moderate Burnout",
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

#### Get Assessment Details

**GET** `/assessments/{assessment_id}/details`

Get detailed assessment information including score breakdown and classification.

**Response:** `200 OK`
```json
{
  "assessment_id": 1,
  "user_id": 1,
  "burnout_score": 68.5,
  "burnout_stage": "Moderate Burnout",
  "score_breakdown": {
    "work_hours": 7.5,
    "sleep_duration": 8.2,
    "sleep_quality": 12.0,
    "emotional_exhaustion": 18.75,
    "motivation": 9.0,
    "screen_time": 7.5,
    "perceived_stress": 7.5
  },
  "explanation": "Your burnout score is 68.5/100. Primary contributing factors: emotional_exhaustion (18.75%), sleep_quality (12.0%), work_hours (7.5%)",
  "classification": {
    "stage": "Moderate Burnout",
    "stage_key": "moderate_burnout",
    "description": "You're experiencing moderate burnout symptoms...",
    "recommendations_level": "intervention",
    "score_range": [51, 75]
  },
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

#### Get User Assessments

**GET** `/assessments/user/{user_id}?skip=0&limit=10`

Get all assessments for a user, ordered by most recent first.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 10)

**Response:** `200 OK`
```json
[
  {
    "assessment_id": 1,
    "user_id": 1,
    "burnout_score": 68.5,
    "burnout_stage": "Moderate Burnout",
    "created_at": "2024-01-15T10:35:00Z"
  }
]
```

---

### Recovery Plans

#### Generate Recovery Plan

**POST** `/recovery/generate`

Generate a new AI-powered recovery plan based on assessment.

**Request Body:**
```json
{
  "user_id": 1,
  "assessment_id": 1
}
```

**Response:** `201 Created`
```json
{
  "plan_id": 1,
  "user_id": 1,
  "recommendations": {
    "daily_actions": [
      "Take 10-minute breaks every 2 hours",
      "Practice deep breathing exercises 3 times daily",
      "Ensure 7-8 hours of sleep"
    ],
    "weekly_goals": [
      "Reduce work hours by 10% if possible",
      "Schedule one day completely off from work"
    ],
    "behavioral_suggestions": [
      "Consider consulting a healthcare professional",
      "Establish clear work boundaries",
      "Prioritize rest and recovery"
    ],
    "caution_notes": [
      "Severe burnout may require professional intervention",
      "Monitor symptoms and seek help if they worsen"
    ],
    "disclaimer": "This is not medical advice. Please consult a healthcare professional for severe symptoms."
  },
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": null
}
```

---

#### Get Latest Recovery Plan

**GET** `/recovery/user/{user_id}/latest`

Get the most recent recovery plan for a user.

**Response:** `200 OK`
```json
{
  "plan_id": 1,
  "user_id": 1,
  "recommendations": { ... },
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": null
}
```

**Error:** `404 Not Found` if no plan exists.

---

#### Get Recovery Plan

**GET** `/recovery/{plan_id}`

Get recovery plan by ID.

**Response:** `200 OK`
```json
{
  "plan_id": 1,
  "user_id": 1,
  "recommendations": { ... },
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": null
}
```

---

#### Regenerate Recovery Plan

**POST** `/recovery/{plan_id}/regenerate`

Regenerate a recovery plan (useful for adaptive updates).

**Response:** `200 OK`
```json
{
  "plan_id": 1,
  "user_id": 1,
  "recommendations": { ... },
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### Progress

#### Create Progress Record

**POST** `/progress/`

Create a new progress record.

**Request Body:**
```json
{
  "user_id": 1,
  "weekly_score": 65.0,
  "completion_status": {
    "daily_0": true,
    "daily_1": false,
    "weekly_0": true
  },
  "user_notes": "Feeling slightly better this week"
}
```

**Response:** `201 Created`
```json
{
  "progress_id": 1,
  "user_id": 1,
  "weekly_score": 65.0,
  "completion_status": { ... },
  "user_notes": "Feeling slightly better this week",
  "timestamp": "2024-01-15T11:00:00Z"
}
```

---

#### Get User Progress

**GET** `/progress/user/{user_id}?skip=0&limit=20`

Get all progress records for a user, ordered by most recent first.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 20)

**Response:** `200 OK`
```json
[
  {
    "progress_id": 1,
    "user_id": 1,
    "weekly_score": 65.0,
    "completion_status": { ... },
    "user_notes": "Feeling slightly better this week",
    "timestamp": "2024-01-15T11:00:00Z"
  }
]
```

---

#### Get Progress Analysis

**GET** `/progress/user/{user_id}/analysis`

Get progress analysis including trend and recommendations.

**Response:** `200 OK`
```json
{
  "current_score": 65.0,
  "current_stage": "Moderate Burnout",
  "progress_analysis": {
    "trend": "improving",
    "change": -3.5,
    "recommendation": "Great progress! Your burnout score has improved...",
    "needs_adjustment": false,
    "previous_score": 68.5,
    "current_score": 65.0
  },
  "progress_history": [
    {
      "progress_id": 1,
      "weekly_score": 65.0,
      "timestamp": "2024-01-15T11:00:00Z",
      "user_notes": "Feeling slightly better this week"
    }
  ]
}
```

**Trend Values:**
- `improving`: Score decreased by ≥5 points
- `declining`: Score increased by ≥5 points
- `stagnant`: Score unchanged for 2+ weeks
- `stable`: Score relatively stable
- `insufficient_data`: Less than 2 assessments

---

#### Get Progress Record

**GET** `/progress/{progress_id}`

Get progress record by ID.

**Response:** `200 OK`
```json
{
  "progress_id": 1,
  "user_id": 1,
  "weekly_score": 65.0,
  "completion_status": { ... },
  "user_notes": "Feeling slightly better this week",
  "timestamp": "2024-01-15T11:00:00Z"
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing rate limiting to prevent abuse.

## API Versioning

The current API version is `1.0.0`. Future versions may be introduced via URL path (e.g., `/api/v2/`) or headers.
