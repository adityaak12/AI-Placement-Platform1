import json
from datetime import datetime
from extensions import db


class CodingProblem(db.Model):
    __tablename__ = 'coding_problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    difficulty = db.Column(db.String(20), default='medium')  # 'easy', 'medium', 'hard'
    category = db.Column(db.String(80), nullable=False, index=True)  # 'Arrays', 'Strings', 'DP', etc.
    description = db.Column(db.Text, nullable=False)
    input_format = db.Column(db.Text, nullable=True)
    output_format = db.Column(db.Text, nullable=True)
    constraints = db.Column(db.Text, nullable=True)
    sample_input = db.Column(db.Text, nullable=True)
    sample_output = db.Column(db.Text, nullable=True)
    test_cases_json = db.Column(db.Text, default='[]')  # JSON array of {input, expected, is_hidden}
    starter_code = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('CodingSubmission', backref='problem', lazy='dynamic', cascade='all, delete-orphan')

    def get_test_cases(self):
        try:
            return json.loads(self.test_cases_json or '[]')
        except Exception:
            return []

    def set_test_cases(self, test_cases_list):
        self.test_cases_json = json.dumps(test_cases_list)

    def to_dict(self, include_test_cases=False):
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'difficulty': self.difficulty,
            'category': self.category,
            'description': self.description,
            'input_format': self.input_format,
            'output_format': self.output_format,
            'constraints': self.constraints,
            'sample_input': self.sample_input,
            'sample_output': self.sample_output,
            'starter_code': self.starter_code or '# Write your solution below\n\ndef solve():\n    pass\n',
        }
        if include_test_cases:
            data['test_cases'] = self.get_test_cases()
        return data

    def __repr__(self):
        return f'<CodingProblem {self.id}: {self.title} [{self.difficulty}]>'


class CodingSubmission(db.Model):
    __tablename__ = 'coding_submissions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id', ondelete='CASCADE'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(30), default='python')
    status = db.Column(db.String(40), default='Pending')  # 'Accepted', 'Wrong Answer', 'Runtime Error', etc.
    passed_tests = db.Column(db.Integer, default=0)
    total_tests = db.Column(db.Integer, default=0)
    score = db.Column(db.Float, default=0.0)
    execution_time_ms = db.Column(db.Float, default=0.0)
    error_message = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'problem_title': self.problem.title if self.problem else None,
            'language': self.language,
            'status': self.status,
            'passed_tests': self.passed_tests,
            'total_tests': self.total_tests,
            'score': self.score,
            'execution_time_ms': self.execution_time_ms,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

    def __repr__(self):
        return f'<CodingSubmission {self.id} User:{self.student_id} Status:{self.status}>'

