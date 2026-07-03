import logging
import jwt
from functools import wraps
from flask import request, jsonify, g
from app.auth.services import AuthService

logger = logging.getLogger('app.auth.decorators')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            logger.warning("Authentication failed: Bearer prefix missing in header")
            return jsonify({
                "error": True,
                "message": "Authentication required. Bearer token missing.",
                "code": "AUTH_REQUIRED"
            }), 401

        token = auth_header.replace('Bearer ', '', 1).strip()
        try:
            user = AuthService.get_user_from_token(token)
            g.current_user = user
        except jwt.ExpiredSignatureError as exc:
            logger.warning("Authentication failed: token has expired: %s", exc)
            return jsonify({
                "error": True,
                "message": "Authentication failed. Token has expired.",
                "code": "TOKEN_EXPIRED"
            }), 401
        except jwt.InvalidTokenError as exc:
            logger.warning("Authentication failed: invalid token: %s", exc)
            return jsonify({
                "error": True,
                "message": "Authentication failed. Token is invalid.",
                "code": "INVALID_TOKEN"
            }), 401
        except Exception as exc:
            logger.exception("Authentication failed due to unexpected error")
            return jsonify({
                "error": True,
                "message": f"Authentication failed: {str(exc)}",
                "code": "AUTH_ERROR"
            }), 401

        return f(*args, **kwargs)
    return decorated_function
