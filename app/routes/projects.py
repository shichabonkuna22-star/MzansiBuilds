"""
MZB_ Project Routes - Create, Update, Milestones
HUMAN_DECISION: Routes follow REST conventions (C# analogy: API controllers)
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.project import MZB_Project
from app.models.milestone import MZB_Milestone
from app.models.comment import MZB_Comment

bp = Blueprint('projects', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    """User's personal dashboard showing their projects"""
    my_projects = MZB_Project.query.filter_by(user_id=current_user.id).order_by(MZB_Project.created_at.desc()).all()
    return render_template('dashboard.html', title='My Dashboard', projects=my_projects)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        stage = request.form.get('stage')
        support_needed = request.form.get('support_needed')
        
        if not title or not description:
            flash('Title and description are required.', 'danger')
            return redirect(url_for('projects.create_project'))
        
        project = MZB_Project(
            title=title,
            description=description,
            stage=stage,
            support_needed=support_needed,
            user_id=current_user.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash(f'Project "{title}" created successfully!', 'success')
        return redirect(url_for('projects.dashboard'))
    
    return render_template('create_project.html', title='Create New Project')

@bp.route('/<int:project_id>')
@login_required
def view_project(project_id):
    project = MZB_Project.query.get_or_404(project_id)
    milestones = project.milestones.order_by(MZB_Milestone.achieved_date.desc()).all()
    # Get all comments for this project (not limited)
    comments = MZB_Comment.query.filter_by(project_id=project_id).order_by(MZB_Comment.created_at.desc()).all()
    return render_template('project_detail.html', title=project.title, project=project, milestones=milestones, comments=comments)

@bp.route('/<int:project_id>/milestone', methods=['POST'])
@login_required
def add_milestone(project_id):
    project = MZB_Project.query.get_or_404(project_id)
    
    # Security: Only project owner can add milestones
    if project.user_id != current_user.id:
        abort(403)
    
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title:
        milestone = MZB_Milestone(
            project_id=project_id,
            title=title,
            description=description
        )
        db.session.add(milestone)
        db.session.commit()
        flash('Milestone added! Progress updated.', 'success')
    
    return redirect(url_for('projects.view_project', project_id=project_id))

@bp.route('/<int:project_id>/complete', methods=['POST'])
@login_required
def complete_project(project_id):
    project = MZB_Project.query.get_or_404(project_id)
    
    if project.user_id != current_user.id:
        abort(403)
    
    project.complete_project()
    db.session.commit()
    flash(f'🎉 Congratulations! "{project.title}" is complete and added to the Celebration Wall!', 'success')
    return redirect(url_for('celebration.wall'))

@bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = MZB_Project.query.get_or_404(project_id)
    
    if project.user_id != current_user.id:
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('projects.dashboard'))