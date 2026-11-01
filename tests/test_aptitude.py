import pytest
from app import create_app
from extensions import db
from models.user import User
from models.question import Question
from models.test import Test, TestQuestion


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_aptitude_question_and_test(app, client):
    with app.app_context():
        q = Question(
            question_text="What is 10 + 20?",
            option_a="10",
            option_b="20",
            option_c="30",
            option_d="40",
            correct_option="C",
            category="aptitude",
            subcategory="quantitative",
            difficulty="easy",
            explanation="10 + 20 = 30."
        )
        db.session.add(q)
        db.session.commit()

        test = Test(
            title="Unit Aptitude Test",
            category="aptitude",
            duration_minutes=10,
            total_marks=10,
            passing_marks=5
        )
        db.session.add(test)
        db.session.commit()

        db.session.add(TestQuestion(test_id=test.id, question_id=q.id, marks=10))
        db.session.commit()

        assert q.id is not None
        assert test.question_count == 1
