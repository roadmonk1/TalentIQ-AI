import logging
from datetime import datetime
from app import db
from app.auth.models import User
from app.common.utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

logger = logging.getLogger('app.auth')


class AuthService:
    @staticmethod
    def register(payload):
        existing_user = User.query.filter_by(email=payload['email'].lower()).first()
        if existing_user:
            logger.warning('Registration rejected for duplicate email', extra={'email': payload['email']})
            raise ValueError('Email already registered')

        user = User(
            full_name=payload['full_name'].strip(),
            email=payload['email'].lower(),
            password_hash=hash_password(payload['password']),
            role=payload.get('role', 'Student'),
        )
        db.session.add(user)
        db.session.commit()
        logger.info('User registered', extra={'user_id': str(user.id), 'email': user.email, 'role': user.role})
        return user

    @staticmethod
    def login(payload):
        user = User.query.filter_by(email=payload['email'].lower()).first()
        if not user or not verify_password(payload['password'], user.password_hash):
            logger.warning('Failed login attempt', extra={'email': payload['email']})
            raise ValueError('Invalid email or password')

        if not user.is_active:
            logger.warning('Inactive user login blocked', extra={'user_id': str(user.id)})
            raise ValueError('Account is inactive')

        user.last_login = datetime.utcnow()
        db.session.commit()
        logger.info('User logged in', extra={'user_id': str(user.id), 'email': user.email})

        return {
            'user': user,
            'access_token': create_access_token(str(user.id), user.role),
            'refresh_token': create_refresh_token(str(user.id)),
        }

    @staticmethod
    def refresh_token(token):
        payload = decode_token(token)
        if payload.get('type') != 'refresh':
            logger.warning('Refresh token rejected due to invalid type', extra={'token_type': payload.get('type')})
            raise ValueError('Invalid token type')

        import uuid
        try:
            user_id = uuid.UUID(payload['sub']) if isinstance(payload['sub'], str) else payload['sub']
        except ValueError:
            user_id = payload['sub']

        user = User.query.get(user_id)
        if not user:
            logger.warning('Refresh token rejected for missing user', extra={'user_id': payload.get('sub')})
            raise ValueError('User not found')

        logger.info('Refresh token used', extra={'user_id': str(user.id)})
        return {
            'access_token': create_access_token(str(user.id), user.role),
            'refresh_token': create_refresh_token(str(user.id)),
        }

    @staticmethod
    def get_user_from_token(token):
        payload = decode_token(token)
        import uuid
        try:
            user_id = uuid.UUID(payload['sub']) if isinstance(payload['sub'], str) else payload['sub']
        except ValueError:
            user_id = payload['sub']

        user = User.query.get(user_id)
        if not user:
            logger.warning('Token lookup failed for missing user', extra={'user_id': payload.get('sub')})
            raise ValueError('User not found')
        return user
