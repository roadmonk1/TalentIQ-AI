import logging
from flask import Blueprint, request, jsonify
from app.mentor.service import MentorService
import app.mentor.adapters as adapters

logger = logging.getLogger('app.mentor.routes')
mentor_bp = Blueprint('mentor', __name__)

@mentor_bp.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    result = MentorService.handle_chat(payload)
    return jsonify(result), 200

@mentor_bp.route('/mission', methods=['POST'])
def mission():
    payload = request.get_json(silent=True) or {}
    result = MentorService.handle_mission(payload)
    return jsonify(result), 200

@mentor_bp.route('/session/<session_id>', methods=['GET'])
def session(session_id):
    result = MentorService.get_session(session_id)
    return jsonify(result), 200

@mentor_bp.route('/context', methods=['GET'])
def context():
    session_id = request.args.get('session_id')
    user_id = request.args.get('user_id')
    result = MentorService.refresh_context({'session_id': session_id, 'user_id': user_id})
    return jsonify(result), 200

@mentor_bp.route('/refresh', methods=['POST'])
def refresh():
    payload = request.get_json(silent=True) or {}
    result = MentorService.refresh_context(payload)
    return jsonify(result), 200

@mentor_bp.route('/health', methods=['GET'])
def health():
    # Provider health check status
    try:
        provider = adapters.provider_factory()
        model = getattr(provider, 'model_name', 'unknown')
        # allow provider to expose a health_check method
        reachable = True
        try:
            if hasattr(provider, 'health_check'):
                reachable = provider.health_check()
        except Exception:
            reachable = False
        status = {
            'active_provider': provider.__class__.__name__,
            'provider_reachable': reachable,
            'model': model,
            'pipeline': 'ok',
        }
        return jsonify(status), 200
    except Exception as exc:
        return jsonify({'active_provider': None, 'provider_reachable': False, 'model': None, 'pipeline': 'degraded', 'error': str(exc)}), 200

@mentor_bp.route('/feedback', methods=['POST'])
def feedback():
    payload = request.get_json(silent=True) or {}
    result = MentorService.submit_feedback(payload)
    return jsonify(result), 200
