# AI-Powered Burnout Detection and Recovery Planning Agent

A comprehensive web application that assesses burnout levels using structured self-report inputs and generates personalized, ethical, non-medical recovery plans using AI.

## 🎯 Project Alignment

This project aligns with **United Nations Sustainable Development Goal (SDG) 3: Good Health and Well-Being**, focusing on mental health awareness and support.

## ⚠️ Important Disclaimer

**This system is NOT a medical diagnostic tool.** It serves as a decision-support and awareness tool only. The system does not perform medical diagnosis and should not replace professional medical or psychological advice.


## ✅ To see final site:
- clone the GitHub repo.
- Go in frontend folder `cd frontend`
- Run this command `npm start`

site will start working on the browser.
---


## 🏗️ System Architecture

```
Frontend (React.js)
    ↓
Backend API (FastAPI)
    ↓
┌─────────────────┬──────────────┬──────────────┐
│ Scoring Engine  │ AI Agent     │ Database     │
│ Classification  │ (LLM)        │ (SQL/PostgreSQL)│
└─────────────────┴──────────────┴──────────────┘
```

**Database:** Uses raw SQL queries (SQLite for development, PostgreSQL/Supabase for production)

## 📁 Project Structure

```
IBM_skill_project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Database schema definitions
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── schema.sql           # SQL schema (SQLite/PostgreSQL)
│   │   ├── schema_postgresql.sql # PostgreSQL-specific schema
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── scoring.py       # Burnout scoring engine
│   │   │   ├── classification.py # Burnout classification
│   │   │   ├── ai_agent.py      # AI recovery planning
│   │   │   └── adaptive.py      # Adaptive follow-up logic
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── assessments.py
│   │   │   ├── recovery.py
│   │   │   └── progress.py
│   │   └── database.py          # Raw SQL database connection
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssessmentForm.jsx
│   │   │   ├── ResultPage.jsx
│   │   │   ├── RecoveryDashboard.jsx
│   │   │   └── ProgressTracking.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── ETHICS.md
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
py -3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# AI Configuration (Google Gemini - Free tier available)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro

# Database Configuration
# For SQLite (default):
DATABASE_URL=sqlite:///./burnout_detection.db

# For Supabase/PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@host:port/database
```

**Getting a Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to your `.env` file

## 📊 Features

1. **Burnout Assessment**: Multi-factor questionnaire with weighted scoring
2. **Burnout Classification**: Automatic categorization (Healthy, Early, Moderate, Severe)
3. **AI Recovery Planning**: Personalized recovery recommendations
4. **Progress Tracking**: Historical data visualization
5. **Adaptive Recommendations**: Dynamic plan adjustments based on progress

## 🔒 Security & Privacy

- Input validation on all endpoints
- SQL injection protection via parameterized queries
- No storage of sensitive personal information
- Ethical AI constraints enforced
- Supports both SQLite (development) and PostgreSQL/Supabase (production)

## 📚 Documentation

- [System Architecture](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Ethical Guidelines](docs/ETHICS.md)
- **[Complete Supabase Deployment Guide](SUPABASE_DEPLOYMENT.md)** - Step-by-step guide for running with Supabase (Backend + Frontend)
- **[Production Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy Frontend to Vercel & Backend to Render

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

This project is for educational and portfolio purposes.

## 🤝 Contributing

This is a capstone project. For questions or improvements, please refer to the project documentation.
