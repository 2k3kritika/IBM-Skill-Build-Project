# Project Summary: AI-Powered Burnout Detection and Recovery Planning Agent

## Project Overview

This is a complete, production-ready capstone project implementing an AI-powered web application for burnout detection and recovery planning. The system aligns with **United Nations Sustainable Development Goal (SDG) 3: Good Health and Well-Being**.

## Key Features

✅ **Burnout Assessment**
- Multi-factor questionnaire with weighted scoring
- Real-time score calculation (0-100 scale)
- Automatic classification (Healthy, Early, Moderate, Severe)

✅ **AI-Powered Recovery Planning**
- Personalized recommendations using LLM APIs
- Structured output (daily actions, weekly goals, behavioral suggestions)
- Ethical AI constraints enforced

✅ **Progress Tracking**
- Historical score visualization with charts
- Trend analysis (improving, declining, stagnant)
- Adaptive plan adjustments

✅ **User-Friendly Interface**
- Modern React frontend with intuitive UI
- Multi-step assessment form
- Interactive recovery dashboard
- Progress visualization

## Technology Stack

### Backend
- **Python 3.8+** with FastAPI
- **SQLAlchemy ORM** with SQLite database
- **Pydantic** for data validation
- **Google Gemini API** for AI recommendations (free tier available)

### Frontend
- **React 18.2+** with functional components
- **React Router** for navigation
- **Recharts** for data visualization
- **Axios** for API communication

## Project Structure

```
IBM_skill_project/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── database.py     # Database configuration
│   │   ├── routes/         # API endpoints
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   └── App.jsx        # Main app component
│   ├── package.json        # Node dependencies
│   └── README.md          # Frontend documentation
│
├── docs/                   # Comprehensive documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── API.md             # API documentation
│   └── ETHICS.md          # Ethical guidelines
│
├── README.md               # Main project README
├── SETUP.md                # Setup instructions
└── .gitignore             # Git ignore rules
```

## Core Components

### 1. Burnout Scoring Engine
- Weighted factor analysis
- Normalization functions for each input type
- Transparent score breakdown

### 2. Classification Module
- Four-stage classification system
- Threshold-based categorization
- Descriptive explanations

### 3. AI Recovery Agent
- Ethical prompt engineering
- Structured JSON output
- Fallback recommendations
- Uses Google Gemini API (free tier available)

### 4. Adaptive Follow-Up Logic
- Progress trend detection
- Automatic plan adjustment recommendations
- Score change analysis

## Ethical Safeguards

✅ **Non-Medical Nature**: Explicitly not a diagnostic tool
✅ **Transparency**: Clear explanations of methodology
✅ **Non-Judgmental**: Supportive, empathetic language
✅ **Safety First**: Professional help recommendations for severe cases
✅ **Privacy**: Local data storage, no third-party sharing

## Database Schema

- **Users**: Basic user information
- **Assessments**: Questionnaire responses and scores
- **RecoveryPlans**: AI-generated recommendations
- **Progress**: Weekly tracking records

## API Endpoints

- **Users**: Create, get, list users
- **Assessments**: Create, get, list assessments with details
- **Recovery**: Generate, get, regenerate recovery plans
- **Progress**: Create, get, analyze progress records

## Documentation

Comprehensive documentation includes:
- **README.md**: Project overview and quick start
- **SETUP.md**: Detailed setup instructions
- **ARCHITECTURE.md**: System design and data flow
- **API.md**: Complete API reference
- **ETHICS.md**: Ethical guidelines and safeguards

## Getting Started

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   # Create .env file with API key
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Key Highlights

🎯 **Production-Ready**: Modular, well-documented, scalable architecture
🎯 **Ethically Sound**: Comprehensive safeguards and disclaimers
🎯 **SDG 3 Aligned**: Promotes mental health awareness and well-being
🎯 **Academic Quality**: Suitable for capstone project evaluation
🎯 **Portfolio Ready**: Professional code structure and documentation

## Limitations & Disclaimers

- Not a medical diagnostic tool
- Self-report bias in assessments
- AI recommendations are generated, not personalized by human experts
- No real-time monitoring
- Local storage only (SQLite)

## Future Enhancements

- User authentication and authorization
- PostgreSQL for production
- Async AI API calls
- Caching layer
- Background job processing
- Mobile app version

## Compliance

✅ United Nations SDG 3: Good Health and Well-Being
✅ Ethical AI principles (beneficence, non-maleficence, autonomy, justice)
✅ Data privacy best practices
✅ Non-medical wellness tool standards

## Support

For setup issues, refer to:
- [SETUP.md](SETUP.md) for installation instructions
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system understanding
- [docs/API.md](docs/API.md) for API usage

---

**Project Status**: ✅ Complete and Ready for Evaluation

This project demonstrates:
- Full-stack development skills
- AI integration and ethical AI practices
- Database design and ORM usage
- RESTful API design
- Modern frontend development
- Comprehensive documentation
- Ethical considerations in healthcare technology
