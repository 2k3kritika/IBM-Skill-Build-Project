# Setup Guide

Complete setup instructions for the AI-Powered Burnout Detection and Recovery Planning Agent.

## Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm or yarn** - Comes with Node.js
- **Google Gemini API Key** (Free tier available) - [Get Gemini API Key](https://makersuite.google.com/app/apikey)

## Step 1: Clone/Download Project

If using git:
```bash
git clone <repository-url>
cd IBM_skill_project
```

Or extract the project files to `IBM_skill_project` directory.

## Step 2: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
# Copy the example file
cp .env.example .env
```

5. Edit `.env` file and add your API key:
```env
# AI Configuration (Google Gemini - Free tier available)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro

# Database Configuration
# For SQLite (development - default):
DATABASE_URL=sqlite:///./burnout_detection.db

# For Supabase/PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@host:port/database
```

**Getting a Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to your `.env` file

6. Initialize database:
```bash
# The database will be created automatically on first run
# For SQLite:
python -c "from app.database import init_db; init_db()"

# For PostgreSQL/Supabase, use schema_postgresql.sql instead
```

7. Start backend server:
```bash
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

You can view API documentation at `http://localhost:8000/docs`

## Step 3: Frontend Setup

1. Open a new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Create `.env` file for custom API URL:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

4. Start frontend development server:
```bash
npm start
```

The frontend will open automatically at `http://localhost:3000`

## Step 4: Verify Installation

1. Backend should be running on port 8000
2. Frontend should be running on port 3000
3. Visit `http://localhost:3000` in your browser
4. You should see the home page

## Troubleshooting

### Backend Issues

**Import Errors:**
```bash
# Make sure you're in the backend directory and virtual environment is activated
pip install -r requirements.txt
```

**Database Errors:**
```bash
# SQLite: Delete existing database and recreate
rm burnout_detection.db
python -c "from app.database import init_db; init_db()"

# PostgreSQL: Check connection string and ensure database exists
# Verify DATABASE_URL format: postgresql://user:password@host:port/database
```

**API Key Errors:**
- Verify your `.env` file exists in the `backend` directory
- Check that `GOOGLE_GEMINI_API_KEY` is set correctly
- Ensure no extra spaces or quotes around the API key
- Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Frontend Issues

**Port Already in Use:**
```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Kill process on port 3000 (macOS/Linux)
lsof -ti:3000 | xargs kill
```

**Module Not Found:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Connection Errors:**
- Verify backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify `REACT_APP_API_URL` in frontend `.env` if set

### Common Issues

**Python Version:**
- Ensure Python 3.8+ is installed: `python --version`
- Use `python3` instead of `python` on macOS/Linux if needed

**Node Version:**
- Ensure Node.js 16+ is installed: `node --version`
- Update Node.js if version is too old

**Virtual Environment:**
- Always activate virtual environment before running backend
- Deactivate with `deactivate` when done

## Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload
   ```

2. **Start Frontend (new terminal):**
   ```bash
   cd frontend
   npm start
   ```

3. **Make Changes:**
   - Backend: Changes auto-reload with `--reload` flag
   - Frontend: Changes auto-reload with React's hot reload

4. **View API Docs:**
   - Visit `http://localhost:8000/docs` for interactive API documentation

## Production Build

### Backend

```bash
cd backend
# Install production dependencies
pip install gunicorn
# Run with Gunicorn (example)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
cd frontend
npm run build
# Serve the build folder with a web server (Nginx, Apache, etc.)
```

## Next Steps

1. Read the [README.md](README.md) for project overview
2. Review [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
3. Check [API.md](docs/API.md) for API documentation
4. Review [ETHICS.md](docs/ETHICS.md) for ethical guidelines

## Getting Help

- Check the documentation in the `docs/` directory
- Review error messages carefully
- Verify all prerequisites are installed
- Ensure environment variables are set correctly

## Supabase Setup (Production)

To use Supabase instead of SQLite:

1. Create a Supabase project at [supabase.com](https://supabase.com)

2. Get your database connection string from Supabase dashboard:
   - Go to Project Settings → Database
   - Copy the connection string (URI format)

3. Update `.env` file:
```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

4. Run PostgreSQL schema:
```bash
# Option 1: Use psql command line
psql $DATABASE_URL -f app/schema_postgresql.sql

# Option 2: Use Python to execute schema
python -c "
from app.database import get_connection
with open('app/schema_postgresql.sql', 'r') as f:
    schema = f.read()
conn = get_connection()
cursor = conn.cursor()
cursor.execute(schema)
conn.commit()
conn.close()
"
```

5. Install PostgreSQL driver (if not already installed):
```bash
pip install psycopg2-binary
```

## Notes

- **SQLite (Development)**: Database file (`burnout_detection.db`) will be created automatically
- **PostgreSQL/Supabase (Production)**: Requires manual database creation and schema execution
- All data is stored in the configured database
- No internet connection required after setup (except for AI API calls)
- API keys should be kept secure and never committed to version control
- The system automatically detects database type from DATABASE_URL
