import pytest
from app import create_app
from extensions import db
from models.coding import CodingProblem
from utils.code_runner import execute_python_code


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_code_runner_execution():
    test_cases = [
        {'input': 'hello\n', 'expected': 'hello', 'is_hidden': False},
        {'input': 'world\n', 'expected': 'world', 'is_hidden': False}
    ]
    code = 'import sys\nprint(sys.stdin.read().strip())'
    result = execute_python_code(code, test_cases)
    assert result['status'] == 'Accepted'
    assert result['passed'] == 2
    assert result['total'] == 2


def test_code_runner_wrong_answer():
    test_cases = [
        {'input': 'hello\n', 'expected': 'world', 'is_hidden': False}
    ]
    code = 'print("wrong")'
    result = execute_python_code(code, test_cases)
    assert result['status'] == 'Wrong Answer'
    assert result['passed'] == 0


def test_coding_problem_model(app):
    with app.app_context():
        problem = CodingProblem(
            title="Test Problem",
            slug="test-problem",
            difficulty="easy",
            category="Arrays",
            description="Sample description"
        )
        problem.set_test_cases([{'input': '1', 'expected': '1', 'is_hidden': False}])
        db.session.add(problem)
        db.session.commit()

        loaded = CodingProblem.query.filter_by(slug="test-problem").first()
        assert loaded is not None
        assert len(loaded.get_test_cases()) == 1
