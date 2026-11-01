import json
from datetime import datetime
from extensions import db


class ResumeAnalysis(db.Model):
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    target_role = db.Column(db.String(100), default='Software Engineer')
    ats_score = db.Column(db.Float, default=0.0)
    matched_skills_json = db.Column(db.Text, default='[]')
    missing_skills_json = db.Column(db.Text, default='[]')
    sections_detected_json = db.Column(db.Text, default='{}')
    feedback_json = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_matched_skills(self):
        try:
            return json.loads(self.matched_skills_json or '[]')
        except Exception:
            return []

    def get_missing_skills(self):
        try:
            return json.loads(self.missing_skills_json or '[]')
        except Exception:
            return []

    def get_feedback(self):
        try:
            return json.loads(self.feedback_json or '{}')
        except Exception:
            return {}

    def get_sections(self):
        try:
            return json.loads(self.sections_detected_json or '{}')
        except Exception:
            return {}

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'original_filename': self.original_filename,
            'target_role': self.target_role,
            'ats_score': self.ats_score,
            'matched_skills': self.get_matched_skills(),
            'missing_skills': self.get_missing_skills(),
            'sections': self.get_sections(),
            'feedback': self.get_feedback(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<ResumeAnalysis {self.id} User:{self.student_id} Score:{self.ats_score}>'

