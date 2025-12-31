# Unified Study Calculator Backend

Pure API backend for the Study Calculator application. Frontend is handled separately by React.

## Features

- **Cost Calculator API**: Calculate study abroad costs
- **Grade Calculator API**: Convert grades to German system
- **User Management**: Store user details and requests
- **Session Management**: Handle user sessions
- **Pure JSON API**: No frontend rendering

## Setup

```bash
cd Unified-Backend
pip install -r requirements.txt
python run.py
```

API runs on `http://localhost:5000`

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/cost-calculator/calculate` - Calculate costs
- `POST /api/cost-calculator/user-details` - Store user data
- `POST /api/cost-calculator/request-callback` - Request callback
- `POST /api/grade-calculator/calculate` - Calculate German grade
- `POST /api/grade-calculator/user-details` - Store user data

## Database

SQLite database with auto-created tables:
- `user_submission`
- `report_submission` 
- `request_call_back`
- `grade_user_submission`