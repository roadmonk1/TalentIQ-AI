import uuid
from datetime import datetime
from app import db


class MentorSession(db.Model):
    __tablename__ = 'mentor_sessions'

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), index=True, nullable=True)
    mode = db.Column(db.String(50), default='Career')
    summary = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = db.relationship('MentorMessage', backref='session', cascade='all, delete-orphan', lazy=True)
    memories = db.relationship('MentorMemory', backref='session', cascade='all, delete-orphan', lazy=True)
    missions = db.relationship('Mission', backref='session', lazy=True)


class MentorMessage(db.Model):
    __tablename__ = 'mentor_messages'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    session_id = db.Column(db.String(100), db.ForeignKey('mentor_sessions.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text, nullable=False)
    meta = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MentorMemory(db.Model):
    __tablename__ = 'mentor_memory'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    session_id = db.Column(db.String(100), db.ForeignKey('mentor_sessions.id', ondelete='CASCADE'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Mission(db.Model):
    __tablename__ = 'missions'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(100), index=True, nullable=True)
    session_id = db.Column(db.String(100), db.ForeignKey('mentor_sessions.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending|accepted|completed|skipped
    schedule = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)


class UserFeedback(db.Model):
    __tablename__ = 'user_feedbacks'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(100), index=True, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=True)
    page = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

