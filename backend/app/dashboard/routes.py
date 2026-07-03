import logging
from flask import Blueprint, jsonify, request, g
from app.dashboard.services import DashboardService
from app.auth.decorators import login_required
from app import db

logger = logging.getLogger('app.dashboard')

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/', methods=['GET'])
@login_required
def get_dashboard():
    user_id = str(g.current_user.id)
    target = request.args.get('target_career', 'default')
    try:
        payload = DashboardService.get_dashboard(user_id=user_id, target_career=target)
    except Exception as exc:
        logger.exception('Failed to build dashboard payload')
        return jsonify({'error': 'Failed to load dashboard'}), 500

    return jsonify({'dashboard': payload}), 200


@dashboard_bp.route('/demo', methods=['GET'])
def get_dashboard_demo():
    try:
        payload = DashboardService.get_dashboard(user_id='demo_user', target_career='frontend')
    except Exception:
        logger.exception('Failed to build demo dashboard payload')
        return jsonify({'error': 'Failed to load demo dashboard'}), 500
    return jsonify({'dashboard': payload}), 200


@dashboard_bp.route('/feedback', methods=['POST'])
@login_required
def submit_general_feedback():
    payload = request.get_json(silent=True) or {}
    rating = payload.get('rating')
    message = payload.get('message')
    page = payload.get('page')
    user_id = str(g.current_user.id)

    if not rating:
        return jsonify({'error': 'Rating is required'}), 400

    try:
        from app.mentor.models import UserFeedback
        fb = UserFeedback(
            user_id=user_id,
            rating=int(rating),
            message=message,
            page=page
        )
        db.session.add(fb)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.exception('Failed to save general user feedback')
        return jsonify({'error': str(exc)}), 500

    return jsonify({'status': 'ok', 'message': 'Feedback received'}), 200


