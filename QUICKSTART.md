# RIAM LMS - Quick Reference

## Fixed Issue
✅ **Login credentials now work!**

The issue was SQLite in-memory database creating separate instances per connection. 
Changed to file-based database: `sqlite:///./riam_lms.db`

## Quick Start

### Option 1: Use the Start Script
```bash
./start.sh
```
Then open http://localhost:5000

### Option 2: Manual Start
```bash
# Terminal 1 - API
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 - UI  
cd ui
pip install -r requirements.txt
python app.py
```

## Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin | Administrator |
| teacher | teacher | Teacher (Dr. Sarah Murphy) |
| teacher2 | teacher2 | Teacher (Prof. Michael O'Brien) |
| student | student | Student (Emma Walsh) |
| student2 | student2 | Student (Liam Kelly) |
| student3 | student3 | Student (Aoife Brennan) |

## URLs

- **Web UI**: http://localhost:5000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What You'll See

### Admin Dashboard
- System statistics
- All users list
- Performance overview
- Musical pieces library

### Teacher Dashboard  
- Add class notes
- Assign tasks
- View recent classes
- Track student progress

### Student Dashboard
- View assigned tasks
- See class feedback
- Track progress
- Access musical pieces

## Troubleshooting

### If login still fails:
```bash
# Delete the old database and restart
cd api
rm -f riam_lms.db
uvicorn app.main:app --reload
```

### Check if services are running:
```bash
# API should be on port 8000
curl http://localhost:8000/health

# UI should be on port 5000
curl http://localhost:5000
```

### View logs:
```bash
# If using start.sh
tail -f api.log
tail -f ui.log
```

## Features Demonstrated

✅ Role-based authentication (JWT)  
✅ Different dashboards per role  
✅ Class session management  
✅ Task assignment & tracking  
✅ Student feedback system  
✅ Musical pieces library  
✅ Responsive design (Tailwind CSS)  
✅ HTMX for seamless updates  
✅ Alpine.js for interactivity  

## Database

The application uses SQLite with a file-based database that persists between restarts.

- **Location**: `api/riam_lms.db`
- **Reset**: Delete the file to start fresh
- **Seed Data**: Auto-created on first start

## Architecture

```
Browser → Flask UI (port 5000) → FastAPI (port 8000) → SQLite DB
                                      ↓
                                   S3 Bucket (for recordings)
```

Enjoy exploring the RIAM Learning Management System! 🎵
