import logging
from flask import Blueprint, request, jsonify, g
from app.mentor.service import MentorService
import app.mentor.adapters as adapters
from app.auth.decorators import login_required

logger = logging.getLogger('app.mentor.routes')
mentor_bp = Blueprint('mentor', __name__)


@mentor_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    payload = request.get_json(silent=True) or {}
    payload['user_id'] = str(g.current_user.id)
    result = MentorService.handle_chat(payload)
    return jsonify(result), 200


@mentor_bp.route('/mission', methods=['POST'])
@login_required
def mission():
    payload = request.get_json(silent=True) or {}
    payload['user_id'] = str(g.current_user.id)
    result = MentorService.handle_mission(payload)
    return jsonify(result), 200


@mentor_bp.route('/session/<session_id>', methods=['GET'])
@login_required
def session(session_id):
    result = MentorService.get_session(session_id)
    return jsonify(result), 200


@mentor_bp.route('/context', methods=['GET'])
@login_required
def context():
    session_id = request.args.get('session_id')
    user_id = str(g.current_user.id)
    result = MentorService.refresh_context({'session_id': session_id, 'user_id': user_id})
    return jsonify(result), 200


@mentor_bp.route('/refresh', methods=['POST'])
@login_required
def refresh():
    payload = request.get_json(silent=True) or {}
    payload['user_id'] = str(g.current_user.id)
    result = MentorService.refresh_context(payload)
    return jsonify(result), 200


@mentor_bp.route('/health', methods=['GET'])
def health():
    db_status = "disconnected"
    provider_status = "unavailable"
    status_val = "degraded"

    # Database connectivity check
    try:
        from app import db
        from sqlalchemy import text
        db.session.execute(text('SELECT 1')).scalar()
        db_status = "connected"
    except Exception as exc:
        logger.exception("Health check failed on database validation query")
        db_status = "disconnected"

    # LLM Mentor Provider check
    try:
        provider = adapters.provider_factory()
        reachable = True
        if hasattr(provider, 'health_check'):
            try:
                reachable = provider.health_check()
            except Exception:
                reachable = False
        if reachable:
            provider_status = "available"
    except Exception as exc:
        logger.exception("Health check failed on provider adapter initialization")
        provider_status = "unavailable"

    if db_status == "connected" and provider_status == "available":
        status_val = "ok"

    return jsonify({
        "status": status_val,
        "database": db_status,
        "provider": provider_status,
        "version": "1.0.0-beta"
    }), 200



@mentor_bp.route('/feedback', methods=['POST'])
@login_required
def feedback():
    payload = request.get_json(silent=True) or {}
    payload['user_id'] = str(g.current_user.id)
    result = MentorService.submit_feedback(payload)
    return jsonify(result), 200
