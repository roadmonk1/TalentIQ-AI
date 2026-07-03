import uuid
from datetime import datetime
from app import db


class ResumeProfile(db.Model):
    __tablename__ = 'resume_profiles'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(100), index=True, nullable=True)
    source = db.Column(db.String(50), default='upload')
    filename = db.Column(db.String(255), nullable=True)
    raw_text = db.Column(db.Text, nullable=True)
    parsed_profile = db.Column(db.JSON, nullable=True)
    meta_json = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to career score snapshots
    scores = db.relationship('CareerScoreSnapshot', backref='profile', cascade='all, delete-orphan', lazy=True)


class CareerScoreSnapshot(db.Model):
    __tablename__ = 'career_score_snapshots'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    profile_id = db.Column(db.Uuid, db.ForeignKey('resume_profiles.id', ondelete='CASCADE'), nullable=False)
    career_score = db.Column(db.Float, nullable=True)
    resume_score = db.Column(db.Float, nullable=True)
    ats_score = db.Column(db.Float, nullable=True)
    breakdown = db.Column(db.JSON, nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)


class TimelineEvent(db.Model):
    __tablename__ = 'timeline_events'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(100), index=True, nullable=True)
    type = db.Column(db.String(100), nullable=False)
    payload = db.Column(db.JSON, nullable=True)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)
