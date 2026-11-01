import pytest
from app import create_app
from extensions import db
from models.user import User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'PlacementAI' in response.data or b'AI Placement Preparation' in response.data


def test_student_registration_and_login(client, app):
    # Register
    res = client.post('/auth/register', data={
        'name': 'Test Candidate',
        'email': 'candidate@test.edu',
        'password': 'password123',
        'confirm_password': 'password123',
        'college': 'Test Tech Institute',
        'degree': 'B.Tech IT',
        'graduation_year': '2026',
        'target_role': 'Software Engineer'
    }, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email='candidate@test.edu').first()
        assert user is not None
        assert user.name == 'Test Candidate'
        assert user.check_password('password123')
        assert not user.check_password('wrongpass')

    # Logout
    logout_res = client.get('/auth/logout', follow_redirects=True)
    assert logout_res.status_code == 200

    # Login
    login_res = client.post('/auth/login', data={
        'email': 'candidate@test.edu',
        'password': 'password123'
    }, follow_redirects=True)
    assert login_res.status_code == 200
    assert b'Welcome back' in login_res.data or b'Test Candidate' in login_res.data
