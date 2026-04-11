"""
MZB_ Route Integration Tests - Fixed for detached instances
"""

import pytest
from app import create_app, db
from app.models.user import MZB_User
from app.models.project import MZB_Project
from app.models.collaboration import MZB_CollaborationRequest

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = MZB_User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        # Refresh to keep the instance attached
        db.session.refresh(user)
        return user

@pytest.fixture
def test_user2(app):
    with app.app_context():
        user = MZB_User(username='testuser2', email='test2@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

def test_index_page_loads(client):
    """Test home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MzansiBuilds' in response.data

def test_register_page_loads(client):
    """Test registration page loads"""
    response = client.get('/auth/register')
    assert response.status_code == 200

def test_login_page_loads(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_user_registration(client):
    """Test user can register successfully"""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'bio': 'Test bio'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_user_login(client, test_user):
    """Test user can login successfully"""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_dashboard_requires_login(client):
    """Test dashboard redirects unauthenticated users"""
    response = client.get('/projects/dashboard', follow_redirects=True)
    assert response.status_code == 200
    # Should show login page
    assert b'Login' in response.data or b'Sign Up' in response.data

def test_create_project_authenticated(client, test_user):
    """Test authenticated user can create project"""
    # Login first
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/projects/create', data={
        'title': 'Test Project',
        'description': 'This is a test project description that is long enough.',
        'stage': 'ideation',
        'support_needed': 'code_review'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_collaboration_request_flow(client, test_user, test_user2):
    """Test full collaboration request flow"""
    # Store user IDs
    owner_id = test_user.id
    requester_id = test_user2.id
    
    # Login as test_user (owner)
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Create project as test_user
    client.post('/projects/create', data={
        'title': 'Collab Test Project',
        'description': 'This is a project that needs collaboration',
        'stage': 'ideation',
        'support_needed': 'collaboration'
    })
    
    # Get the project
    with client.application.app_context():
        project = MZB_Project.query.filter_by(title='Collab Test Project').first()
        assert project is not None
        project_id = project.id
        
        # Logout
        client.get('/auth/logout')
        
        # Login as test_user2 (requester)
        client.post('/auth/login', data={
            'email': 'test2@example.com',
            'password': 'password123'
        })
        
        # Send collaboration request
        response = client.post(f'/feed/project/{project_id}/raise-hand', data={
            'message': 'I would like to collaborate on this project'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check if request was created
        request = MZB_CollaborationRequest.query.filter_by(
            project_id=project_id,
            requester_id=requester_id
        ).first()
        
        assert request is not None
        assert request.status == 'pending'
        
        request_id = request.id
        
        # Logout and login as owner to respond
        client.get('/auth/logout')
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Accept the request
        response = client.post(f'/feed/request/{request_id}/respond', data={
            'action': 'accept'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify status updated
        request = MZB_CollaborationRequest.query.get(request_id)
        assert request.status == 'accepted'

def test_request_count_endpoint(client, test_user, test_user2):
    """Test request count AJAX endpoint"""
    # Login as test_user (owner)
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Create project
    client.post('/projects/create', data={
        'title': 'Count Test Project',
        'description': 'Testing request count',
        'stage': 'ideation'
    })
    
    with client.application.app_context():
        project = MZB_Project.query.filter_by(title='Count Test Project').first()
        assert project is not None
        
        # Create a collaboration request using IDs
        request = MZB_CollaborationRequest(
            project_id=project.id,
            requester_id=test_user2.id,
            owner_id=test_user.id,
            message='Test message',
            status='pending'
        )
        db.session.add(request)
        db.session.commit()
        
        # Test the count endpoint
        response = client.get('/feed/request-count')
        assert response.status_code == 200
        assert b'count' in response.data