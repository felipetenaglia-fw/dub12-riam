import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'riam-ui-secret-key-change-me')

# API Configuration
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_headers():
    """Get authorization headers."""
    token = session.get('access_token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}


@app.route('/')
def index():
    """Home page - redirects to login or dashboard."""
    if 'access_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/login',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                session['access_token'] = data['access_token']
                
                # Get user info
                user_response = requests.get(
                    f'{API_BASE_URL}/auth/me',
                    headers=get_headers()
                )
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    session['user'] = user_data
                    return redirect(url_for('dashboard'))
            
            return render_template('login.html', error='Invalid credentials')
        except Exception as e:
            return render_template('login.html', error=f'Error connecting to API: {str(e)}')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - role-based content."""
    user = session.get('user', {})
    role = user.get('role', '')
    
    return render_template('dashboard.html', user=user, role=role)


# API proxy endpoints for HTMX
@app.route('/api/classes')
@login_required
def api_classes():
    """Get classes."""
    response = requests.get(f'{API_BASE_URL}/classes', headers=get_headers())
    return jsonify(response.json()), response.status_code


@app.route('/api/tasks')
@login_required
def api_tasks():
    """Get tasks."""
    response = requests.get(f'{API_BASE_URL}/tasks', headers=get_headers())
    return jsonify(response.json()), response.status_code


@app.route('/api/pieces')
@login_required
def api_pieces():
    """Get musical pieces."""
    response = requests.get(f'{API_BASE_URL}/pieces', headers=get_headers())
    return jsonify(response.json()), response.status_code


@app.route('/api/users')
@login_required
def api_users():
    """Get users (admin only)."""
    response = requests.get(f'{API_BASE_URL}/users', headers=get_headers())
    return jsonify(response.json()), response.status_code


@app.route('/api/performance/overview')
@login_required
def api_performance_overview():
    """Get performance overview (admin only)."""
    response = requests.get(f'{API_BASE_URL}/performance/overview', headers=get_headers())
    return jsonify(response.json()), response.status_code


@app.route('/api/ai-coach', methods=['POST'])
@login_required
def api_ai_coach():
    """Submit audio to AI coach for analysis."""
    try:
        # Get form data
        audio_file = request.files.get('audio_file')
        piece_name = request.form.get('piece_name')
        composer = request.form.get('composer')
        student_notes = request.form.get('student_notes')
        
        if not audio_file:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        # Prepare multipart form data for backend API
        files = {'audio_file': (audio_file.filename, audio_file.stream, audio_file.content_type)}
        data = {}
        
        if piece_name:
            data['piece_name'] = piece_name
        if composer:
            data['composer'] = composer
        if student_notes:
            data['student_notes'] = student_notes
        
        # Forward to backend API
        response = requests.post(
            f'{API_BASE_URL}/ai-coach/analyze',
            headers={'Authorization': get_headers()['Authorization']},
            files=files,
            data=data,
            timeout=120  # 2 minutes timeout for AI processing
        )
        
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'Request timed out. The audio file may be too large.'}), 504
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
