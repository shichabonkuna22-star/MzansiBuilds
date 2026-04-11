"""
MZB_ Comment Model - Feed interaction
"""

from app import db
from app.models.user import get_sast_time

class MZB_Comment(db.Model):
    __tablename__ = 'MZB_comment'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('MZB_project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('MZB_user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=get_sast_time)
    
    # Relationships
    project = db.relationship('MZB_Project', back_populates='comments')
    author = db.relationship('MZB_User', backref='user_comments')
    
    def __repr__(self):
        return f'<MZB_Comment by User {self.user_id} on Project {self.project_id}>'