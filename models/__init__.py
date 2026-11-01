from extensions import db
from models.user import User, load_user
from models.question import Question
from models.test import Test, TestQuestion
from models.coding import CodingProblem, CodingSubmission
from models.interview import InterviewSession
from models.resume import ResumeAnalysis
from models.result import TestResult
from models.progress import StudentProgress
from models.recommendation import Recommendation

__all__ = [
    'db',
    'User',
    'load_user',
    'Question',
    'Test',
    'TestQuestion',
    'CodingProblem',
    'CodingSubmission',
    'InterviewSession',
    'ResumeAnalysis',
    'TestResult',
    'StudentProgress',
    'Recommendation',
]

