import logging
from flask import Blueprint, jsonify, request
from app.dashboard.services import DashboardService

logger = logging.getLogger('app.dashboard')

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/', methods=['GET'])
def get_dashboard():
    user_id = request.args.get('user_id')
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

