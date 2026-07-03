import pytest
import json
import uuid
from app import app, db
from app.auth.models import User
from app.common.utils import create_access_token


@pytest.fixture(autouse=True)
def app_context():
    """Push app context and build all tables before tests run."""
    app.config['TESTING'] = True
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    yield
    db.session.rollback()
    # Cleanup any API test users that might remain
    try:
        User.query.filter(User.email.like("api_test_%")).delete(synchronize_session=False)
        db.session.commit()
    except Exception:
        db.session.rollback()
    db.session.remove()
    ctx.pop()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_header():
    """Generates a valid authorization header for a dummy test user."""
    user = User(
        full_name="API Test User",
        email="api_test_user@example.com",
        password_hash="dummy_hash",
        role="Student"
    )
    db.session.add(user)
    db.session.commit()
    
    token = create_access_token(str(user.id), user.role)
    header = {"Authorization": f"Bearer {token}"}
    yield header


def test_dashboard_route_without_token_returns_401(client):
    response = client.get('/api/dashboard/')
    assert response.status_code == 401
    data = json.loads(response.data.decode('utf-8'))
    assert data['error'] is True
    assert data['code'] == "AUTH_REQUIRED"


def test_dashboard_route_with_valid_token_succeeds(client, auth_header):
    response = client.get('/api/dashboard/', headers=auth_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'dashboard' in data
    assert data['dashboard'].get('empty_state') is True


def test_public_demo_routes_still_work_without_token(client):
    # Verify dashboard demo endpoint
    response_dash_demo = client.get('/api/dashboard/demo')
    assert response_dash_demo.status_code == 200
    data_dash = json.loads(response_dash_demo.data.decode('utf-8'))
    assert 'dashboard' in data_dash
    assert data_dash['dashboard']['user']['id'] == "demo_user"

    # Verify resume demo endpoint
    response_resume_demo = client.get('/api/resumes/demo')
    assert response_resume_demo.status_code == 200
    data_resume = json.loads(response_resume_demo.data.decode('utf-8'))
    assert data_resume['status'] == 'ok'
    assert 'profile' in data_resume


def test_protected_resumes_upload_without_token_returns_401(client):
    response = client.post('/api/resumes/upload', data={})
    assert response.status_code == 401
    data = json.loads(response.data.decode('utf-8'))
    assert data['error'] is True
    assert data['code'] == "AUTH_REQUIRED"


def test_protected_mentor_endpoints_without_token_returns_401(client):
    res_chat = client.post('/api/mentor/chat', json={})
    assert res_chat.status_code == 401
    
    res_ctx = client.get('/api/mentor/context?session_id=123')
    assert res_ctx.status_code == 401


def test_feedback_route_without_token_returns_401(client):
    response = client.post('/api/dashboard/feedback', json={'rating': 5, 'message': 'Great!'})
    assert response.status_code == 401
    data = json.loads(response.data.decode('utf-8'))
    assert data['error'] is True
    assert data['code'] == "AUTH_REQUIRED"


def test_feedback_route_with_valid_token_succeeds(client, auth_header):
    from app.mentor.models import UserFeedback
    response = client.post(
        '/api/dashboard/feedback',
        headers=auth_header,
        json={'rating': 4, 'message': 'Excellent beta features!', 'page': '/dashboard'}
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['status'] == 'ok'
    
    # Assert database record was created
    fb = UserFeedback.query.filter_by(message='Excellent beta features!').first()
    assert fb is not None
    assert fb.rating == 4
    assert fb.page == '/dashboard'

