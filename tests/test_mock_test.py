import pytest
from app import create_app
from extensions import db
from models.test import Test
from ai.resume_analyzer import analyze_resume_content
from ai.mock_interview import evaluate_candidate_answer


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_resume_analyzer_ai():
    resume_text = """
    Aditya Madne
    Email: student@placement.edu
    Education: B.Tech in Computer Science
    Projects: Developed a full stack web platform using Python, SQL, and React with Git version control.
    Skills: Python, Java, Data Structures, Algorithms, SQL, Git, OOPs, Docker.
    Certifications: Completed AWS Cloud certification.
    """
    analysis = analyze_resume_content(resume_text, target_role="Software Engineer")
    assert analysis['ats_score'] > 50
    assert 'python' in analysis['matched_skills']
    assert 'sql' in analysis['matched_skills']
    assert analysis['sections_detected']['education'] is True


def test_interview_evaluator_ai():
    q = {
        'id': 1,
        'question': 'Explain OOP principles',
        'keywords': ['encapsulation', 'inheritance', 'polymorphism', 'abstraction'],
        'ideal_answer': 'The four principles are Encapsulation, Inheritance, Polymorphism, Abstraction.'
    }
    ans = "The four principles of Object Oriented Programming are Encapsulation, Abstraction, Inheritance, and Polymorphism. For example, polymorphism allows method overriding."
    eval_res = evaluate_candidate_answer(q, ans)
    assert eval_res['score'] >= 60
    assert len(eval_res['keywords_matched']) >= 3
