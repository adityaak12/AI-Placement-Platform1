from datetime import datetime
from extensions import db


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'practice', 'coding', 'resume', 'interview', 'mock_test'
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    suggested_action = db.Column(db.String(255), nullable=True)
    action_url = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(20), default='medium')  # 'high', 'medium', 'low'
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'recommendation_type': self.recommendation_type,
            'title': self.title,
            'description': self.description,
            'reason': self.reason,
            'suggested_action': self.suggested_action,
            'action_url': self.action_url,
            'priority': self.priority,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Recommendation {self.id} User:{self.student_id} [{self.priority}] {self.title}>'

