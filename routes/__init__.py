from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.aptitude_routes import aptitude_bp
from routes.technical_routes import technical_bp
from routes.coding_routes import coding_bp
from routes.mock_test_routes import mock_test_bp
from routes.interview_routes import interview_bp
from routes.resume_routes import resume_bp
from routes.recommendation_routes import recommendation_bp
from routes.admin_routes import admin_bp

__all__ = [
    'auth_bp',
    'student_bp',
    'aptitude_bp',
    'technical_bp',
    'coding_bp',
    'mock_test_bp',
    'interview_bp',
    'resume_bp',
    'recommendation_bp',
    'admin_bp',
]

