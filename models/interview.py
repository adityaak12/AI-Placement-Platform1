import json
from datetime import datetime
from extensions import db


class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    interview_type = db.Column(db.String(30), nullable=False)  # 'hr' or 'technical'
    target_role = db.Column(db.String(100), default='Software Engineer')
    status = db.Column(db.String(20), default='in_progress')  # 'in_progress', 'completed'
    messages_json = db.Column(db.Text, default='[]')
    current_question_index = db.Column(db.Integer, default=0)
    overall_score = db.Column(db.Float, default=0.0)
    technical_score = db.Column(db.Float, default=0.0)
    communication_score = db.Column(db.Float, default=0.0)
    confidence_score = db.Column(db.Float, default=0.0)
    feedback_json = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def get_messages(self):
        try:
            return json.loads(self.messages_json or '[]')
        except Exception:
            return []

    def set_messages(self, messages_list):
        self.messages_json = json.dumps(messages_list)

    def append_message(self, role, content, feedback=None):
        msgs = self.get_messages()
        msg_obj = {'role': role, 'content': content, 'timestamp': datetime.utcnow().isoformat()}
        if feedback:
            msg_obj['feedback'] = feedback
        msgs.append(msg_obj)
        self.set_messages(msgs)

    def get_feedback(self):
        try:
            return json.loads(self.feedback_json or '{}')
        except Exception:
            return {}

    def set_feedback(self, feedback_dict):
        self.feedback_json = json.dumps(feedback_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'interview_type': self.interview_type,
            'target_role': self.target_role,
            'status': self.status,
            'messages': self.get_messages(),
            'current_question_index': self.current_question_index,
            'overall_score': self.overall_score,
            'technical_score': self.technical_score,
            'communication_score': self.communication_score,
            'confidence_score': self.confidence_score,
            'feedback': self.get_feedback(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<InterviewSession {self.id} {self.interview_type} Score:{self.overall_score}>'

