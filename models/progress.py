from datetime import datetime
from extensions import db


class StudentProgress(db.Model):
    __tablename__ = 'student_progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(80), nullable=True)
    tests_taken = db.Column(db.Integer, default=0)
    questions_attempted = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    accuracy_percentage = db.Column(db.Float, default=0.0)
    time_spent_seconds = db.Column(db.Integer, default=0)
    mastery_level = db.Column(db.String(30), default='Beginner')  # Beginner, Intermediate, Advanced
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_accuracy(self):
        if self.questions_attempted > 0:
            self.accuracy_percentage = round((self.correct_count / self.questions_attempted) * 100, 1)
        else:
            self.accuracy_percentage = 0.0

        if self.accuracy_percentage >= 80 and self.questions_attempted >= 15:
            self.mastery_level = 'Advanced'
        elif self.accuracy_percentage >= 50 and self.questions_attempted >= 5:
            self.mastery_level = 'Intermediate'
        else:
            self.mastery_level = 'Beginner'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'category': self.category,
            'subcategory': self.subcategory,
            'tests_taken': self.tests_taken,
            'questions_attempted': self.questions_attempted,
            'correct_count': self.correct_count,
            'accuracy_percentage': round(self.accuracy_percentage, 1),
            'mastery_level': self.mastery_level,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

    def __repr__(self):
        return f'<StudentProgress User:{self.student_id} {self.category}/{self.subcategory} Acc:{self.accuracy_percentage}%>'

