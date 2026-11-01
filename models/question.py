from datetime import datetime
from extensions import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_option = db.Column(db.String(5), nullable=False)  # 'A', 'B', 'C', or 'D'
    category = db.Column(db.String(50), nullable=False, index=True)  # 'aptitude' or 'technical'
    subcategory = db.Column(db.String(80), nullable=False, index=True)  # 'quantitative', 'logical', 'verbal', 'dsa', 'dbms', 'os', 'cn'
    difficulty = db.Column(db.String(20), default='medium')  # 'easy', 'medium', 'hard'
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_answer=False):
        data = {
            'id': self.id,
            'question_text': self.question_text,
            'options': {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d,
            },
            'category': self.category,
            'subcategory': self.subcategory,
            'difficulty': self.difficulty,
        }
        if include_answer:
            data['correct_option'] = self.correct_option
            data['explanation'] = self.explanation
        return data

    def __repr__(self):
        return f'<Question {self.id}: {self.category}/{self.subcategory} [{self.difficulty}]>'

