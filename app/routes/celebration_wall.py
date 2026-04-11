"""
MZB_ Celebration Wall - Completed projects showcase
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.models.project import MZB_Project

bp = Blueprint('celebration', __name__)

@bp.route('/wall')
@login_required
def wall():
    """Celebration Wall showing all completed projects"""
    completed_projects = MZB_Project.query.filter_by(is_completed=True).order_by(MZB_Project.completed_at.desc()).all()
    return render_template('celebration_wall.html', title='Celebration Wall 🏆', projects=completed_projects)