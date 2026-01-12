# Complete Guide: Running the Project with Supabase

This guide provides step-by-step instructions for setting up and running the entire AI-Powered Burnout Detection application with Supabase (PostgreSQL) as the database, including how the backend and frontend work together.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Supabase Setup](#supabase-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [How Backend and Frontend Work Together](#how-backend-and-frontend-work-together)
8. [Testing the Integration](#testing-the-integration)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This application consists of:
- **Frontend**: React.js application running on `http://localhost:3000`
- **Backend**: FastAPI REST API running on `http://localhost:8000`
- **Database**: Supabase (PostgreSQL) hosted in the cloud
- **AI Service**: Google Gemini API for generating recovery plans

### Architecture Flow

```
User Browser (Frontend)
    ↓ HTTP Requests
React.js App (localhost:3000)
    ↓ REST API Calls
FastAPI Backend (localhost:8000)
    ↓ SQL Queries
Supabase PostgreSQL Database (Cloud)
    ↓ AI API Calls
Google Gemini API (Cloud)
```

---

## ✅ Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
   - Check: `python --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **Node.js 16+** and npm installed
   - Check: `node --version` and `npm --version`
   - Download: [nodejs.org](https://nodejs.org/)

3. **Supabase Account** (free tier available)
   - Sign up: [supabase.com](https://supabase.com)

4. **Google Gemini API Key** (free tier available)
   - Get key: [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Git** (optional, for cloning the repository)

---

## 🗄️ Supabase Setup

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click **"New Project"**
3. Fill in project details:
   - **Name**: `burnout-detection` (or your preferred name)
   - **Database Password**: Choose a strong password (⚠️ **SAVE THIS!**)
   - **Region**: Choose closest to your location
4. Click **"Create new project"**
5. Wait 2-3 minutes for the project to be provisioned

### Step 2: Get Database Connection String

1. In Supabase dashboard, go to **Project Settings** → **Database**
2. Scroll to **Connection string** section
3. Select **URI** tab
4. Copy the connection string (it looks like):
   ```
   postgresql://postgres.DATABASELINK:ENCODED_PASSWORD@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require
   WORKED PERFECTLY WITH RAILWAY
   ```
5. Replace `[YOUR-PASSWORD]` with your actual database password
6. **Save this connection string** - you'll need it for the backend

### Step 3: Create Database Schema

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Open `backend/app/schema_postgresql.sql` from your project
4. Copy the entire contents
5. Paste into the SQL Editor
6. Click **"Run"** (or press `Ctrl+Enter` / `Cmd+Enter`)
7. You should see "Success. No rows returned" - this means tables were created successfully

**Verify tables were created:**
- Go to **Table Editor** in Supabase dashboard
- You should see 4 tables: `users`, `assessments`, `recovery_plans`, `progress`

---

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Google Generative AI (for Gemini API)
- psycopg2 (PostgreSQL driver)
- Other required packages

### Step 4: Configure Environment Variables

Create a `.env` file in the `backend` directory:

**Windows:**
```bash
type nul > .env
notepad .env
```

**macOS/Linux:**
```bash
touch .env
nano .env
```

Add the following content (replace with your actual values):

```env
# Google Gemini API Configuration
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro

# Supabase Database Configuration
DATABASE_URL=postgresql://postgres:your_password@db.xxxxx.supabase.co:5432/postgres
```

**Important:**
- Replace `your_gemini_api_key_here` with your actual Google Gemini API key
- Replace the entire `DATABASE_URL` with your Supabase connection string (with password included)
- Never commit the `.env` file to git (it's already in `.gitignore`)

### Step 5: Verify Database Connection

Test that your backend can connect to Supabase:

```bash
python -c "from app.database import get_connection; conn = get_connection(); print('✅ Connected to Supabase successfully!'); conn.close()"
```

If you see "✅ Connected to Supabase successfully!", you're good to go!

### Step 6: Start Backend Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open** - the backend needs to keep running.

**Test the backend:**
- Open browser: `http://localhost:8000`
- You should see: `{"message":"AI-Powered Burnout Detection...","version":"1.0.0","docs":"/docs"}`
- API documentation: `http://localhost:8000/docs`

---

## 🎨 Frontend Setup

### Step 1: Open a New Terminal

**Keep the backend running** in the first terminal, and open a **new terminal window**.

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

```bash
npm install
```

This installs:
- React and React DOM
- React Router
- Axios (for API calls)
- Other React dependencies

### Step 4: Configure Frontend (Optional)

The frontend is already configured to connect to `http://localhost:8000/api` by default.

If you need to change the API URL, create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Step 5: Start Frontend Development Server

```bash
npm start
```

The frontend will:
- Start on `http://localhost:3000`
- Automatically open in your browser
- Show hot-reload for code changes

You should see:
```
Compiled successfully!

You can now view burnout-detection in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

---

## 🚀 Running the Application

### Both Servers Must Be Running

You need **two terminal windows**:

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Access the Application

1. **Frontend**: Open `http://localhost:3000` in your browser
2. **Backend API Docs**: Open `http://localhost:8000/docs` for interactive API testing

---

## 🔄 How Backend and Frontend Work Together

### Request Flow Example: Creating a User

1. **User fills out form** in React frontend (`localhost:3000`)
   - Enters name, age range, occupation type
   - Clicks "Continue to Assessment"

2. **Frontend sends HTTP POST request** to backend:
   ```javascript
   POST http://localhost:8000/api/users/
   Body: {
     "name": "John Doe",
     "age_range": "26-35",
     "occupation_type": "professional"
   }
   ```

3. **Backend receives request** at `backend/app/routes/users.py`:
   - Validates data using Pydantic schemas
   - Connects to Supabase database
   - Executes SQL INSERT query
   - Returns created user data

4. **Backend sends response** back to frontend:
   ```json
   {
     "user_id": 1,
     "name": "John Doe",
     "age_range": "26-35",
     "occupation_type": "professional",
     "created_at": "2024-01-15T10:30:00"
   }
   ```

5. **Frontend receives response**:
   - Stores user_id in state
   - Navigates to assessment form
   - User can now complete the burnout assessment

### Complete User Journey Flow

```
┌─────────────────┐
│  User Browser   │
│  (localhost:3000)│
└────────┬────────┘
         │
         │ 1. User submits form
         ▼
┌─────────────────┐
│  React Frontend │
│  (AssessmentForm)│
└────────┬────────┘
         │
         │ 2. HTTP POST /api/users/
         │    (via axios)
         ▼
┌─────────────────┐
│  FastAPI Backend│
│  (localhost:8000)│
│  routes/users.py│
└────────┬────────┘
         │
         │ 3. SQL INSERT INTO users
         │    (via psycopg2)
         ▼
┌─────────────────┐
│  Supabase DB    │
│  (PostgreSQL)   │
│  users table    │
└────────┬────────┘
         │
         │ 4. Returns user_id
         │
         ▼
┌─────────────────┐
│  Backend        │
│  Returns JSON   │
└────────┬────────┘
         │
         │ 5. HTTP 201 Response
         │
         ▼
┌─────────────────┐
│  Frontend       │
│  Stores user_id │
│  Shows Step 2   │
└─────────────────┘
```

### API Endpoints Used by Frontend

| Frontend Action | Backend Endpoint | Method | Purpose |
|----------------|------------------|--------|---------|
| Create User | `/api/users/` | POST | Register new user |
| Create Assessment | `/api/assessments/` | POST | Submit burnout assessment |
| Generate Recovery Plan | `/api/recovery/generate` | POST | Get AI-generated recovery plan |
| Get Latest Plan | `/api/recovery/user/{id}/latest` | GET | Retrieve user's recovery plan |
| Track Progress | `/api/progress/` | POST | Record weekly progress |
| Get Progress | `/api/progress/user/{id}` | GET | View progress history |

### CORS Configuration

The backend is configured to accept requests from the frontend:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows the React app to make API calls to the backend.

---

## 🧪 Testing the Integration

### Test 1: Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test 2: Create User via API

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "age_range": "26-35",
    "occupation_type": "professional"
  }'
```

Expected response:
```json
{
  "user_id": 1,
  "name": "Test User",
  "age_range": "26-35",
  "occupation_type": "professional",
  "created_at": "2024-01-15T10:30:00"
}
```

### Test 3: Frontend-Backend Connection

1. Open `http://localhost:3000` in browser
2. Fill out user information form
3. Click "Continue to Assessment"
4. Check browser console (F12) for any errors
5. Check backend terminal for request logs

### Test 4: Verify Data in Supabase

1. Go to Supabase dashboard → **Table Editor**
2. Click on **users** table
3. You should see the user you just created
4. Repeat for `assessments`, `recovery_plans`, `progress` tables

---

## 🔍 Troubleshooting

### Backend Issues

**Problem: Backend won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check if virtual environment is activated
# You should see (venv) in terminal prompt

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Database connection error**
```bash
# Verify DATABASE_URL in .env file
# Make sure password is correct
# Test connection:
python -c "from app.database import get_connection; get_connection()"
```

**Problem: "Module not found" errors**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Port 8000 already in use**
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux: Find and kill process
lsof -ti:8000 | xargs kill
```

### Frontend Issues

**Problem: Frontend won't start**
```bash
# Check Node version
node --version  # Should be 16+

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem: "Cannot connect to server" error**
- Verify backend is running on `http://localhost:8000`
- Check browser console (F12) for detailed error
- Verify CORS settings in `backend/app/main.py`

**Problem: Port 3000 already in use**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill
```

### Supabase Issues

**Problem: "Connection refused"**
- Verify Supabase project is active (not paused)
- Check connection string format
- Ensure password is URL-encoded if it contains special characters

**Problem: "Table does not exist"**
- Run the schema creation again in Supabase SQL Editor
- Verify you used `schema_postgresql.sql` (not `schema.sql`)

**Problem: "Authentication failed"**
- Reset database password in Supabase dashboard
- Update DATABASE_URL in `.env` file

### Integration Issues

**Problem: CORS errors in browser**
- Verify backend CORS settings allow `http://localhost:3000`
- Check backend is running
- Clear browser cache

**Problem: API calls return 404**
- Verify backend routes are correct
- Check API base URL in `frontend/src/services/api.js`
- Ensure backend server is running

**Problem: Data not saving**
- Check backend terminal for errors
- Verify Supabase connection string
- Check browser console for API errors
- Verify database schema was created

---

## 📝 Quick Reference

### Starting the Application

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

### Important URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Environment Variables

**Backend `.env`:**
```env
GOOGLE_GEMINI_API_KEY=your_key
GEMINI_MODEL_NAME=gemini-pro
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

**Frontend `.env` (optional):**
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Database Tables

- `users` - User information
- `assessments` - Burnout assessments
- `recovery_plans` - AI-generated recovery plans
- `progress` - User progress tracking

---

## 🎓 Next Steps

1. **Explore the API**: Visit `http://localhost:8000/docs` for interactive API documentation
2. **Test the Application**: Complete a full assessment flow
3. **Monitor Supabase**: Check Supabase dashboard for data
4. **Review Code**: Explore `backend/app/routes/` and `frontend/src/components/`
5. **Read Documentation**: Check `docs/` folder for detailed architecture

---

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Google Gemini API](https://ai.google.dev/docs)

---

## ✅ Checklist

Before running the application, ensure:

- [ ] Supabase project created
- [ ] Database schema executed in Supabase
- [ ] Backend `.env` file configured with Supabase connection string
- [ ] Backend `.env` file configured with Google Gemini API key
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend server running (`uvicorn app.main:app --reload`)
- [ ] Frontend server running (`npm start`)
- [ ] Both servers accessible (backend: 8000, frontend: 3000)
- [ ] Database connection verified
- [ ] Test user creation successful

---

**Happy Coding! 🚀**

If you encounter any issues not covered here, check the main [README.md](README.md) or [SETUP.md](SETUP.md) files for more information.
