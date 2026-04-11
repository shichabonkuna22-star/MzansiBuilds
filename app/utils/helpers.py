"""
MZB_ Helper Functions
HUMAN_DECISION: Reusable utilities for the entire application
AI_ASSIST: Following DRY (Don't Repeat Yourself) principle
"""

import os
import re
from datetime import datetime
from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
import pytz

def get_sast_time():
    """Return current time in South African Standard Time"""
    sast = pytz.timezone('Africa/Johannesburg')
    return datetime.now(sast)

def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    if not filename:
        return False
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_email(email):
    """Basic email validation (pattern matching)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Username: 3-20 chars, alphanumeric + underscore only"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def flash_errors(form):
    """Flash all form validation errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.replace("_", " ").title()}: {error}', 'danger')

def requires_project_owner(project_id_param='project_id'):
    """Decorator to ensure current user owns the project"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.models.project import MZB_Project
            project_id = kwargs.get(project_id_param)
            if project_id:
                project = MZB_Project.query.get(project_id)
                if not project:
                    flash('Project not found.', 'danger')
                    return redirect(url_for('projects.dashboard'))
                if project.user_id != current_user.id:
                    flash('You do not have permission to modify this project.', 'danger')
                    return redirect(url_for('projects.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_input(text):
    """Basic input sanitization (remove dangerous characters)"""
    if not text:
        return text
    # Remove potential script tags and dangerous characters
    dangerous = ['<script', '</script>', 'javascript:', 'onclick', 'onerror']
    for item in dangerous:
        text = text.replace(item, '')
    return text.strip()

def format_datetime_sast(dt):
    """Format datetime for display in SAST"""
    if not dt:
        return 'N/A'
    return dt.strftime('%d %b %Y at %H:%M') + ' SAST'

def truncate_text(text, max_length=150):
    """Truncate text to max length with ellipsis"""
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def get_project_stage_icon(stage):
    """Return emoji icon for project stage"""
    icons = {
        'ideation': '🌱',
        'mvp': '⚙️',
        'growth': '🚀',
        'live': '🏁',
        'completed': '✅'
    }
    return icons.get(stage, '📁')

def get_support_icon(support_type):
    """Return emoji icon for support type"""
    icons = {
        'code_review': '👥',
        'ui_help': '🎨',
        'debugging': '🐛',
        'scaling': '📈',
        'collaboration': '🤝'
    }
    return icons.get(support_type, '💡')