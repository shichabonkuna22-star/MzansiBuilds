"""
MZB_ Project Model - With relationships for templates
"""

from app import db
from datetime import datetime
import pytz

def get_sast_time():
    sast = pytz.timezone('Africa/Johannesburg')
    return datetime.now(sast)

class MZB_Project(db.Model):
    __tablename__ = 'MZB_project'
    
    STAGE_IDEATION = 'ideation'
    STAGE_MVP = 'mvp'
    STAGE_GROWTH = 'growth'
    STAGE_LIVE = 'live'
    STAGE_COMPLETED = 'completed'
    
    STAGE_CHOICES = [
        (STAGE_IDEATION, '🌱 Ideation'),
        (STAGE_MVP, '⚙️ MVP'),
        (STAGE_GROWTH, '🚀 Growth'),
        (STAGE_LIVE, '🏁 Live'),
        (STAGE_COMPLETED, '✅ Completed')
    ]
    
    SUPPORT_CODE_REVIEW = 'code_review'
    SUPPORT_UI_HELP = 'ui_help'
    SUPPORT_DEBUGGING = 'debugging'
    SUPPORT_SCALING = 'scaling'
    SUPPORT_COLLABORATION = 'collaboration'
    
    SUPPORT_CHOICES = [
        (SUPPORT_CODE_REVIEW, '👥 Code Review'),
        (SUPPORT_UI_HELP, '🎨 UI/UX Help'),
        (SUPPORT_DEBUGGING, '🐛 Debugging'),
        (SUPPORT_SCALING, '📈 Scaling Advice'),
        (SUPPORT_COLLABORATION, '🤝 Collaboration')
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    stage = db.Column(db.String(20), nullable=False, default=STAGE_IDEATION)
    support_needed = db.Column(db.String(30), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('MZB_user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_sast_time)
    updated_at = db.Column(db.DateTime, default=get_sast_time, onupdate=get_sast_time)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships for templates
    milestones = db.relationship('MZB_Milestone', back_populates='project', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('MZB_Comment', back_populates='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def complete_project(self):
        self.stage = self.STAGE_COMPLETED
        self.is_completed = True
        self.completed_at = get_sast_time()
    
    def get_stage_display(self):
        return dict(self.STAGE_CHOICES).get(self.stage, self.stage)
    
    def get_support_display(self):
        return dict(self.SUPPORT_CHOICES).get(self.support_needed, self.support_needed or 'No support needed')
    
    def __repr__(self):
        return f'<Project {self.title}>'