from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' or 'admin'
    college = db.Column(db.String(150), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    target_role = db.Column(db.String(100), default='Software Engineer', nullable=True)
    skills = db.Column(db.Text, nullable=True)  # Comma-separated or text
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    test_results = db.relationship('TestResult', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    coding_submissions = db.relationship('CodingSubmission', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    resume_analyses = db.relationship('ResumeAnalysis', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    interview_sessions = db.relationship('InterviewSession', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    progress_records = db.relationship('StudentProgress', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'college': self.college,
            'degree': self.degree,
            'graduation_year': self.graduation_year,
            'target_role': self.target_role,
            'skills': [s.strip() for s in (self.skills or '').split(',') if s.strip()],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

