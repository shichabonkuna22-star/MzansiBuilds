"""
MZB_ Milestone Model - Track progress updates
"""

from app import db
from app.models.user import get_sast_time

class MZB_Milestone(db.Model):
    __tablename__ = 'MZB_milestone'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('MZB_project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    achieved_date = db.Column(db.DateTime, default=get_sast_time)
    created_at = db.Column(db.DateTime, default=get_sast_time)
    
    # Relationship back to project
    project = db.relationship('MZB_Project', back_populates='milestones')
    
    def __repr__(self):
        return f'<MZB_Milestone {self.title}>'