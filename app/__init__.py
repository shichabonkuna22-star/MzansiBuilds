"""
MZB_ Application Factory - Creates and configures the Flask app
HUMAN_DECISION: Using app factory pattern for better testing and configuration
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import models here to avoid circular imports
    from app.models.user import MZB_User
    from app.models.project import MZB_Project
    from app.models.milestone import MZB_Milestone
    from app.models.comment import MZB_Comment
    from app.models.collaboration import MZB_CollaborationRequest
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return MZB_User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import auth, projects, feed, celebration
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(projects.bp, url_prefix='/projects')
    app.register_blueprint(feed.bp, url_prefix='/feed')
    app.register_blueprint(celebration.bp, url_prefix='/celebration')
    
    # Root route - Landing page (accessible to everyone)
    @app.route('/')
    def index():
        from flask_login import current_user
        # Render the index page for everyone
        # If user is logged in, we can pass their info to the template
        return render_template('index.html', title='MzansiBuilds - Build in Public', current_user=current_user)
    
    return app