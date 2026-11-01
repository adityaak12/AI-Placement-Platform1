from datetime import datetime
from extensions import db


class Test(db.Model):
    __test__ = False
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # 'aptitude', 'technical', 'mock_test'
    subcategory = db.Column(db.String(80), nullable=True)
    duration_minutes = db.Column(db.Integer, default=30)
    total_marks = db.Column(db.Integer, default=100)
    passing_marks = db.Column(db.Integer, default=40)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    test_questions = db.relationship('TestQuestion', backref='test', lazy='joined', cascade='all, delete-orphan', order_by='TestQuestion.order_num')
    results = db.relationship('TestResult', backref='test', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def question_count(self):
        return len(self.test_questions)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'duration_minutes': self.duration_minutes,
            'total_marks': self.total_marks,
            'passing_marks': self.passing_marks,
            'question_count': self.question_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Test {self.id}: {self.title} ({self.category})>'


class TestQuestion(db.Model):
    __test__ = False
    __tablename__ = 'test_questions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    order_num = db.Column(db.Integer, default=0)
    marks = db.Column(db.Integer, default=1)

    question = db.relationship('Question', lazy='joined')

    def __repr__(self):
        return f'<TestQuestion Test:{self.test_id} Question:{self.question_id}>'
