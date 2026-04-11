"""
MZB_ Feed Routes - With proper data loading
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import MZB_User
from app.models.project import MZB_Project
from app.models.comment import MZB_Comment
from app.models.collaboration import MZB_CollaborationRequest

bp = Blueprint('feed', __name__)

@bp.route('/')
@login_required
def live_feed():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    projects = MZB_Project.query.filter(
        MZB_Project.user_id != current_user.id
    ).order_by(MZB_Project.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('live_feed.html', title='Live Feed', projects=projects)

@bp.route('/project/<int:project_id>/comment', methods=['POST'])
@login_required
def add_comment(project_id):
    content = request.form.get('content')
    
    if not content:
        flash('Comment cannot be empty.', 'warning')
        return redirect(request.referrer or url_for('feed.live_feed'))
    
    comment = MZB_Comment(
        project_id=project_id,
        user_id=current_user.id,
        content=content
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment added!', 'success')
    return redirect(request.referrer or url_for('feed.live_feed'))

@bp.route('/project/<int:project_id>/raise-hand', methods=['POST'])
@login_required
def raise_hand(project_id):
    try:
        project = MZB_Project.query.get_or_404(project_id)
        
        if project.user_id == current_user.id:
            flash('You cannot request collaboration on your own project.', 'warning')
            return redirect(request.referrer or url_for('feed.live_feed'))
        
        message = request.form.get('message', '')
        if not message:
            message = f"{current_user.username} would like to collaborate on {project.title}"
        
        existing = MZB_CollaborationRequest.query.filter_by(
            project_id=project_id,
            requester_id=current_user.id
        ).first()
        
        if existing:
            flash(f'You already have a {existing.status} request for this project.', 'warning')
            return redirect(request.referrer or url_for('feed.live_feed'))
        
        new_request = MZB_CollaborationRequest(
            project_id=project_id,
            requester_id=current_user.id,
            owner_id=project.user_id,
            message=message,
            status='pending'
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        owner = MZB_User.query.get(project.user_id)
        flash(f'🤚 Request sent to {owner.username}!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash('Failed to send request. Please try again.', 'danger')
    
    return redirect(request.referrer or url_for('feed.live_feed'))

@bp.route('/my-requests')
@login_required
def my_requests():
    requests = MZB_CollaborationRequest.query.filter_by(
        owner_id=current_user.id
    ).order_by(
        MZB_CollaborationRequest.created_at.desc()
    ).all()
    
    # Load related data
    for req in requests:
        req.requester = MZB_User.query.get(req.requester_id)
        req.project = MZB_Project.query.get(req.project_id)
    
    return render_template('my_requests.html', title='Collaboration Requests', requests=requests)

@bp.route('/request/<int:request_id>/respond', methods=['POST'])
@login_required
def respond_to_request(request_id):
    try:
        collab_request = MZB_CollaborationRequest.query.get_or_404(request_id)
        
        if collab_request.owner_id != current_user.id:
            flash('Permission denied.', 'danger')
            return redirect(url_for('feed.my_requests'))
        
        action = request.form.get('action')
        requester = MZB_User.query.get(collab_request.requester_id)
        
        if action == 'accept':
            collab_request.status = 'accepted'
            db.session.commit()
            flash(f'✅ You accepted {requester.username}\'s collaboration request!', 'success')
        elif action == 'reject':
            collab_request.status = 'rejected'
            db.session.commit()
            flash(f'❌ You declined {requester.username}\'s request.', 'info')
        else:
            flash('Invalid action.', 'danger')
            
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash('Error processing your response.', 'danger')
    
    return redirect(url_for('feed.my_requests'))

@bp.route('/request-count')
@login_required
def request_count():
    count = MZB_CollaborationRequest.query.filter_by(
        owner_id=current_user.id,
        status='pending'
    ).count()
    return jsonify({'count': count})