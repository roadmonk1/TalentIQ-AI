import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from app.common.logging import configure_logging

load_dotenv()
configure_logging()

from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "https://talent-iq-ai-nu.vercel.app",
        "http://localhost:5173"
    ]}},
    supports_credentials=True
)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')

# Database selection: prefer DATABASE_URL (PostgreSQL), otherwise fall back to a local SQLite file for development
database_url = os.getenv('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    _db_backend = 'PostgreSQL'
else:
    # default local sqlite file inside project for easy dev runs
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'dev.sqlite')
    sqlite_uri = f"sqlite:///{os.path.abspath(sqlite_path)}"
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
    _db_backend = 'SQLite (dev fallback)'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 900))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
app.config['RATELIMIT_STORAGE_URL'] = os.getenv('RATELIMIT_STORAGE_URL', os.getenv('REDIS_URL', 'memory://'))


from flask_migrate import Migrate

db = SQLAlchemy(app)
limiter = Limiter(key_func=get_remote_address, app=app, default_limits=['200 per day', '50 per hour'])
migrate = Migrate(app, db)

# Import routes
from app.auth.routes import auth_bp
from app.dashboard.routes import dashboard_bp
from app.resume_pipeline.routes import resume_bp
from app.mentor.routes import mentor_bp

# Import all models for SQLAlchemy/Alembic discovery
from app.auth.models import User
from app.resume_pipeline.models import ResumeProfile, CareerScoreSnapshot, TimelineEvent
from app.mentor.models import MentorSession, MentorMessage, MentorMemory, Mission, UserFeedback

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(resume_bp, url_prefix='/api/resumes')
app.register_blueprint(mentor_bp, url_prefix='/api/mentor')

with app.app_context():
    db.create_all()


def _startup_report():
    """Print a short environment readiness report to stdout."""
    checks = {}

    # Database check
    try:
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
        checks['Database'] = (True, _db_backend)
    except Exception as exc:
        checks['Database'] = (False, str(exc))

    # Authentication check
    try:
        from app.auth.services import AuthService  # noqa: F401
        checks['Authentication'] = (True, 'AuthService available')
    except Exception as exc:
        checks['Authentication'] = (False, str(exc))

    # TalentParse Engine
    try:
        from app.resume_pipeline.service import TalentParseService  # noqa: F401
        checks['TalentParse Engine'] = (True, 'TalentParseService available')
    except Exception as exc:
        checks['TalentParse Engine'] = (False, str(exc))

    # TalentCore Engine (CareerIntel)
    try:
        from app.career_intel.service import CareerIntelService  # noqa: F401
        checks['TalentCore Engine'] = (True, 'CareerIntelService available')
    except Exception as exc:
        checks['TalentCore Engine'] = (False, str(exc))

    # Dashboard API (service)
    try:
        from app.dashboard.services import DashboardService  # noqa: F401
        checks['Dashboard API'] = (True, 'DashboardService available')
    except Exception as exc:
        checks['Dashboard API'] = (False, str(exc))

    # Resume Upload API (blueprint registration)
    try:
        checks['Resume Upload API'] = ('resume_pipeline' in app.blueprints, 'blueprints: ' + ','.join(list(app.blueprints.keys())))
    except Exception as exc:
        checks['Resume Upload API'] = (False, str(exc))

    # Print report
    print('\n=== TalentIQ-AI Startup Environment Report ===')
    for key, val in checks.items():
        ok = val[0] is True
        status = 'READY' if ok else 'NOT READY'
        detail = val[1] if isinstance(val[1], str) else str(val[1])
        print(f"- {key}: {status} — {detail}")
    print('=============================================\n')


_startup_report()

__all__ = ['app', 'db']
