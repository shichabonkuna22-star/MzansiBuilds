"""
MZB_ Form Unit Tests - Testing validation logic
HUMAN_DECISION: TDD approach - testing forms independently
"""

import pytest
from app import create_app
from app.forms import RegistrationForm, LoginForm, ProjectForm, CommentForm

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    return app

def test_registration_form_valid(app):
    """Test valid registration data passes validation"""
    with app.test_request_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is True

def test_registration_form_invalid_email(app):
    """Test invalid email fails validation"""
    with app.test_request_context():
        form = RegistrationForm(
            username='testuser',
            email='not-an-email',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is False
        assert 'email' in form.errors

def test_registration_form_password_mismatch(app):
    """Test password mismatch fails validation"""
    with app.test_request_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='different'
        )
        assert form.validate() is False
        assert 'confirm_password' in form.errors

def test_registration_form_short_password(app):
    """Test password too short fails validation"""
    with app.test_request_context():
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='123',
            confirm_password='123'
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_registration_form_short_username(app):
    """Test username too short fails validation"""
    with app.test_request_context():
        form = RegistrationForm(
            username='ab',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is False
        assert 'username' in form.errors

def test_login_form_valid(app):
    """Test valid login form"""
    with app.test_request_context():
        form = LoginForm(
            email='test@example.com',
            password='password123'
        )
        assert form.validate() is True

def test_login_form_missing_email(app):
    """Test missing email fails"""
    with app.test_request_context():
        form = LoginForm(
            email='',
            password='password123'
        )
        assert form.validate() is False
        assert 'email' in form.errors

def test_project_form_valid(app):
    """Test valid project creation form"""
    with app.test_request_context():
        form = ProjectForm(
            title='My Awesome Project',
            description='This is a detailed description of my project...',
            stage='ideation'
        )
        assert form.validate() is True

def test_project_form_missing_title(app):
    """Test missing title fails validation"""
    with app.test_request_context():
        form = ProjectForm(
            title='',
            description='Description here',
            stage='ideation'
        )
        assert form.validate() is False
        assert 'title' in form.errors

def test_project_form_short_description(app):
    """Test description too short fails"""
    with app.test_request_context():
        form = ProjectForm(
            title='My Project',
            description='Too short',
            stage='ideation'
        )
        assert form.validate() is False
        assert 'description' in form.errors

def test_comment_form_valid(app):
    """Test valid comment"""
    with app.test_request_context():
        form = CommentForm(content='This is a great project!')
        assert form.validate() is True

def test_comment_form_empty(app):
    """Test empty comment fails"""
    with app.test_request_context():
        form = CommentForm(content='')
        assert form.validate() is False
        assert 'content' in form.errors