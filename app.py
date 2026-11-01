import os
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from config import config_by_name
from extensions import db, login_manager
from database.db import init_db
from routes import (
    auth_bp,
    student_bp,
    aptitude_bp,
    technical_bp,
    coding_bp,
    mock_test_bp,
    interview_bp,
    resume_bp,
    recommendation_bp,
    admin_bp
)


def create_app(config_name=None):
    """Application factory for AI Placement Preparation Platform."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(aptitude_bp)
    app.register_blueprint(technical_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(mock_test_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(admin_bp)

    # Landing page route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('student.dashboard'))
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Auto-initialize database & seed data
    init_db(app)

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
