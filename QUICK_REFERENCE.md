# Quick Reference Guide

## Common Commands

### Backend

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Initialize database
python -c "from app.database import init_db; init_db()"
```

### Frontend

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## API Endpoints Quick Reference

### Base URL
```
http://localhost:8000/api
```

### Users
- `POST /users/` - Create user
- `GET /users/{id}` - Get user
- `GET /users/` - List users

### Assessments
- `POST /assessments/` - Create assessment
- `GET /assessments/{id}` - Get assessment
- `GET /assessments/{id}/details` - Get detailed assessment
- `GET /assessments/user/{user_id}` - Get user assessments

### Recovery Plans
- `POST /recovery/generate` - Generate plan
- `GET /recovery/user/{user_id}/latest` - Get latest plan
- `GET /recovery/{plan_id}` - Get plan
- `POST /recovery/{plan_id}/regenerate` - Regenerate plan

### Progress
- `POST /progress/` - Create progress record
- `GET /progress/user/{user_id}` - Get user progress
- `GET /progress/user/{user_id}/analysis` - Get progress analysis
- `GET /progress/{id}` - Get progress record

## Environment Variables

### Backend (.env)
```env
# AI Configuration (Google Gemini - Free tier available)
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro

# SQLite (development):
DATABASE_URL=sqlite:///./burnout_detection.db

# PostgreSQL/Supabase (production):
# DATABASE_URL=postgresql://user:password@host:port/database
```

### Frontend (.env) - Optional
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Burnout Score Ranges

- **0-25**: Healthy
- **26-50**: Early Burnout
- **51-75**: Moderate Burnout
- **76-100**: Severe Burnout

## Assessment Factors

1. Daily work/study hours (0-24)
2. Sleep duration (0-24 hours)
3. Sleep quality (1-5 scale)
4. Emotional exhaustion (1-5 scale)
5. Motivation level (1-5 scale)
6. Screen time (0-24 hours)
7. Perceived stress (1-5 scale)

## File Locations

### Backend
- Main app: `backend/app/main.py`
- Models: `backend/app/models.py`
- Routes: `backend/app/routes/`
- Services: `backend/app/services/`
- Database: `backend/burnout_detection.db` (created automatically)

### Frontend
- Main app: `frontend/src/App.jsx`
- Components: `frontend/src/components/`
- API service: `frontend/src/services/api.js`
- Styles: `frontend/src/index.css`

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Check .env file exists and has API key

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Install dependencies: `npm install`
- Check if port 3000 is available

### API errors
- Verify backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify API key in .env file

### Database errors
- SQLite: Delete `burnout_detection.db` and restart
- PostgreSQL: Check connection string in .env
- Verify psycopg2-binary is installed for PostgreSQL
- Check database schema is initialized

## Development Tips

1. **Backend auto-reload**: Use `--reload` flag with uvicorn
2. **Frontend hot reload**: Automatic with `npm start`
3. **API testing**: Use http://localhost:8000/docs for interactive API docs
4. **Database inspection**: Use SQLite browser or command line
5. **Logs**: Check terminal output for errors

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can create a user
- [ ] Can submit assessment
- [ ] Can view results
- [ ] Can generate recovery plan
- [ ] Can view progress tracking
- [ ] Charts display correctly
- [ ] API documentation accessible at /docs

## Ports

- **Frontend**: 3000
- **Backend**: 8000
- **API Docs**: http://localhost:8000/docs

## Important Notes

- **SQLite**: Database is created automatically on first run
- **PostgreSQL/Supabase**: Requires manual schema setup (see SUPABASE_SETUP.md)
- All data stored in configured database (SQLite or PostgreSQL)
- API keys should never be committed to git
- Virtual environment should be activated before running backend
- Both servers must run simultaneously for full functionality
- System automatically detects database type from DATABASE_URL
