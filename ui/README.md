# RIAM LMS - User Interface

Simple web interface for the RIAM Learning Management System API.

## Features

- **Role-Based Dashboards**
  - Admin: View all users, stats, and system overview
  - Teacher: Manage classes, assign tasks, track students
  - Student: View tasks, class feedback, and progress

- **Modern UI**
  - Built with Tailwind CSS for responsive design
  - HTMX for seamless interactions
  - Alpine.js for reactive components

## Quick Start

1. **Install dependencies:**
```bash
cd ui
pip install -r requirements.txt
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env to point to your API (default: http://localhost:8000)
```

3. **Run the UI:**
```bash
python app.py
```

4. **Access the application:**
Open http://localhost:5000 in your browser

## Login Credentials

Use the same mock credentials as the API:
- **Admin**: admin / admin
- **Teacher**: teacher / teacher
- **Student**: student / student

## Tech Stack

- **Flask**: Lightweight Python web framework
- **HTMX**: Modern interactions without heavy JavaScript
- **Alpine.js**: Minimal reactive framework
- **Tailwind CSS**: Utility-first CSS framework

## Configuration

Edit `.env` file:
```
API_BASE_URL=http://localhost:8000  # Your API endpoint
SECRET_KEY=your-secret-key-here     # Flask session secret
```

## Development

The UI runs independently from the API. Make sure the API is running first:

```bash
# Terminal 1: Start API
cd api
uvicorn app.main:app --reload

# Terminal 2: Start UI
cd ui
python app.py
```

## Project Structure

```
ui/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base layout
│   ├── login.html       # Login page
│   └── dashboard.html   # Role-based dashboard
└── static/
    └── css/
        └── style.css    # Custom styles
```

## Features by Role

### Admin Dashboard
- System statistics (students, teachers, classes, tasks)
- View all users with roles
- Performance overview
- Musical pieces library

### Teacher Dashboard
- Quick actions (add class notes, assign tasks)
- Recent classes with student feedback
- Assigned tasks overview
- Student progress tracking
- Musical pieces library

### Student Dashboard
- Task progress overview
- My active tasks with details
- Recent class feedback from teachers
- Musical pieces library

## API Integration

The UI proxies requests to the FastAPI backend. All authentication is handled via JWT tokens stored in Flask sessions.

## Production Deployment

For production:
1. Set strong `SECRET_KEY` in environment
2. Set `FLASK_ENV=production`
3. Use a production WSGI server (e.g., Gunicorn)
4. Configure `API_BASE_URL` to your deployed API

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
