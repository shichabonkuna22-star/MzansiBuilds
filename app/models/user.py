"""
MZB_ User Model - With relationships
"""

from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash

def get_sast_time():
    sast = pytz.timezone('Africa/Johannesburg')
    return datetime.now(sast)

class MZB_User(UserMixin, db.Model):
    __tablename__ = 'MZB_user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(256), default='default-avatar.png')
    bio = db.Column(db.String(500), default='Developer building in public on MzansiBuilds')
    created_at = db.Column(db.DateTime, default=get_sast_time)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    projects = db.relationship('MZB_Project', backref='owner', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_profile_image_url(self):
        from flask import url_for
        if self.profile_image and self.profile_image != 'default-avatar.png':
            return url_for('static', filename=f'uploads/{self.profile_image}')
        return url_for('static', filename='img/default-avatar.png')
    
    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return MZB_User.query.get(int(user_id))