import json
from datetime import datetime
from extensions import db


class TestResult(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'aptitude', 'technical', 'mock_test'
    score = db.Column(db.Float, default=0.0)
    total_marks = db.Column(db.Float, default=100.0)
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    incorrect_answers = db.Column(db.Integer, default=0)
    unanswered = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0.0)
    time_taken_seconds = db.Column(db.Integer, default=0)
    passed = db.Column(db.Boolean, default=False)
    answers_json = db.Column(db.Text, default='{}')
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_answers(self):
        try:
            return json.loads(self.answers_json or '{}')
        except Exception:
            return {}

    def set_answers(self, answers_dict):
        self.answers_json = json.dumps(answers_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'test_id': self.test_id,
            'test_title': self.test.title if self.test else None,
            'category': self.category,
            'score': self.score,
            'total_marks': self.total_marks,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'incorrect_answers': self.incorrect_answers,
            'unanswered': self.unanswered,
            'percentage': round(self.percentage, 1),
            'time_taken_seconds': self.time_taken_seconds,
            'passed': self.passed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<TestResult {self.id} Student:{self.student_id} Score:{self.score}/{self.total_marks}>'

