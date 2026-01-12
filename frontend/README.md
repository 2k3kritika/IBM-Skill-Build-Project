# Frontend - Burnout Detection & Recovery

React frontend for the AI-Powered Burnout Detection and Recovery Planning Agent.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the frontend directory (optional):

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (irreversible)

## Project Structure

```
src/
├── components/
│   ├── AssessmentForm.jsx    # Multi-step assessment form
│   ├── ResultPage.jsx        # Assessment results display
│   ├── RecoveryDashboard.jsx # Recovery plan dashboard
│   └── ProgressTracking.jsx  # Progress tracking with charts
├── services/
│   └── api.js                # API service layer
├── App.jsx                   # Main app component with routing
├── index.js                  # React entry point
└── index.css                 # Global styles
```

## Features

- User registration and assessment
- Burnout score visualization
- AI-generated recovery plans
- Progress tracking with charts
- Responsive design

## Dependencies

- React 18.2+
- React Router DOM 6.20+
- Axios 1.6+
- Recharts 2.10+
