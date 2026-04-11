"""
MZB_ Unit Tests - Test-Driven Development evidence
HUMAN_DECISION: Tests written BEFORE implementation logic
"""

import pytest
from app import create_app, db
from app.models.user import MZB_User, get_sast_time
from app.models.project import MZB_Project

@pytest.fixture
def app():
    app = create_app('config.Config')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(app):
    """Test that user can be created with proper password hashing"""
    with app.app_context():
        user = MZB_User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.check_password('password123') is True
        assert user.check_password('wrong') is False

def test_project_creation(app):
    """Test that project can be created and linked to user"""
    with app.app_context():
        user = MZB_User(username='builder', email='builder@example.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        project = MZB_Project(
            title='Test Project',
            description='Building something awesome',
            stage='ideation',
            user_id=user.id
        )
        db.session.add(project)
        db.session.commit()
        
        assert project.title == 'Test Project'
        assert project.owner.username == 'builder'

def test_project_completion(app):
    """Test that completing a project sets correct flags"""
    with app.app_context():
        user = MZB_User(username='finisher', email='finisher@example.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        project = MZB_Project(title='Finish Me', description='Almost done', user_id=user.id)
        db.session.add(project)
        db.session.commit()
        
        assert project.is_completed is False
        
        project.complete_project()
        db.session.commit()
        
        assert project.is_completed is True
        assert project.stage == 'completed'
        assert project.completed_at is not None