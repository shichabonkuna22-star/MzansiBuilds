"""
MZB_ Collaboration Request Model - Simple collaboration
"""

from app import db
from datetime import datetime
import pytz

def get_sast_time():
    sast = pytz.timezone('Africa/Johannesburg')
    return datetime.now(sast)

class MZB_CollaborationRequest(db.Model):
    __tablename__ = 'MZB_collaboration_request'
    
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('MZB_project.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('MZB_user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('MZB_user.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=get_sast_time)
    
    def __repr__(self):
        return f'<CollaborationRequest {self.id}>'