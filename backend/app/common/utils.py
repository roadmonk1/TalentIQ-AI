import os
import re
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from flask import current_app


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(user_id: str, role: str) -> str:
    payload = {
        'sub': str(user_id),
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
        'iat': datetime.now(timezone.utc),
        'type': 'access',
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def create_refresh_token(user_id: str) -> str:
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(seconds=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']),
        'iat': datetime.now(timezone.utc),
        'type': 'refresh',
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])


def is_valid_email(email: str) -> bool:
    pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return bool(re.fullmatch(pattern, email))
