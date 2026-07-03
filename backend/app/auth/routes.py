import logging
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.auth.schemas import RegisterSchema, LoginSchema, RefreshSchema
from app.auth.services import AuthService
from app import limiter

logger = logging.getLogger('app.auth')

auth_bp = Blueprint('auth', __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()
refresh_schema = RefreshSchema()


@auth_bp.route('/register', methods=['POST'])
@limiter.limit('10 per minute')
def register():
    try:
        payload = register_schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({'error': 'Validation failed', 'details': exc.messages}), 400

    try:
        user = AuthService.register(payload)
    except ValueError as exc:
        logger.warning('Registration endpoint failed', extra={'reason': str(exc)})
        return jsonify({'error': str(exc)}), 409

    return jsonify({'message': 'User registered successfully', 'user': user.to_public_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
@limiter.limit('10 per minute')
def login():
    try:
        payload = login_schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({'error': 'Validation failed', 'details': exc.messages}), 400

    try:
        result = AuthService.login(payload)
    except ValueError as exc:
        logger.warning('Login endpoint failed', extra={'reason': str(exc)})
        return jsonify({'error': str(exc)}), 401

    return jsonify({
        'message': 'Login successful',
        'user': result['user'].to_public_dict(),
        'access_token': result['access_token'],
        'refresh_token': result['refresh_token'],
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@limiter.limit('10 per minute')
def refresh():
    try:
        payload = refresh_schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({'error': 'Validation failed', 'details': exc.messages}), 400

    try:
        result = AuthService.refresh_token(payload['refresh_token'])
    except Exception as exc:
        logger.warning('Refresh endpoint failed', extra={'reason': str(exc)})
        return jsonify({'error': str(exc)}), 401

    return jsonify({'access_token': result['access_token'], 'refresh_token': result['refresh_token']}), 200


@auth_bp.route('/me', methods=['GET'])
def current_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '', 1)
    if not token:
        return jsonify({'error': 'Missing token'}), 401

    try:
        user = AuthService.get_user_from_token(token)
    except Exception as exc:
        logger.warning('Current user endpoint failed', extra={'reason': str(exc)})
        return jsonify({'error': str(exc)}), 401

    return jsonify({'user': user.to_public_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200
