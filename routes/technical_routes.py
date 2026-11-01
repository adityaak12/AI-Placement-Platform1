import json
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from extensions import db
from models.question import Question
from models.test import Test, TestQuestion
from models.result import TestResult
from models.progress import StudentProgress
from utils.decorators import student_required

technical_bp = Blueprint('technical', __name__, url_prefix='/technical')


@technical_bp.route('/')
@student_required
def index():
    tests = Test.query.filter_by(category='technical', is_active=True).all()
    subcategories = ['dsa', 'dbms', 'os', 'cn', 'programming']
    counts = {
        sub: Question.query.filter_by(category='technical', subcategory=sub).count()
        for sub in subcategories
    }
    return render_template('technical/index.html', tests=tests, counts=counts)


@technical_bp.route('/practice')
@student_required
def practice():
    sub = request.args.get('sub', 'all')
    diff = request.args.get('difficulty', 'all')

    query = Question.query.filter_by(category='technical')
    if sub != 'all':
        query = query.filter_by(subcategory=sub)
    if diff != 'all':
        query = query.filter_by(difficulty=diff)

    questions = query.limit(25).all()
    return render_template('technical/practice.html', questions=questions, selected_sub=sub, selected_diff=diff)


@technical_bp.route('/test/<int:test_id>')
@student_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = [tq.question for tq in test.test_questions]
    return render_template('technical/test.html', test=test, questions=questions)


@technical_bp.route('/submit/<int:test_id>', methods=['POST'])
@student_required
def submit_test(test_id):
    test = Test.query.get_or_404(test_id)
    test_questions = test.test_questions

    user_answers = {}
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    total_score = 0.0

    for tq in test_questions:
        q = tq.question
        ans = request.form.get(f'q_{q.id}', '').strip().upper()
        user_answers[str(q.id)] = ans

        if not ans:
            unanswered_count += 1
        elif ans == q.correct_option:
            correct_count += 1
            total_score += tq.marks
        else:
            incorrect_count += 1

    total_q = len(test_questions)
    percentage = (total_score / test.total_marks * 100) if test.total_marks > 0 else 0.0
    passed = total_score >= test.passing_marks
    time_taken = int(request.form.get('time_taken', 0))

    result = TestResult(
        student_id=current_user.id,
        test_id=test.id,
        category='technical',
        score=round(total_score, 1),
        total_marks=test.total_marks,
        total_questions=total_q,
        correct_answers=correct_count,
        incorrect_answers=incorrect_count,
        unanswered=unanswered_count,
        percentage=round(percentage, 1),
        time_taken_seconds=time_taken,
        passed=passed,
        answers_json=json.dumps(user_answers)
    )
    db.session.add(result)

    # Update StudentProgress
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        category='technical',
        subcategory=test.subcategory or 'core_cs'
    ).first()

    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            category='technical',
            subcategory=test.subcategory or 'core_cs'
        )
        db.session.add(progress)

    progress.tests_taken += 1
    progress.questions_attempted += total_q
    progress.correct_count += correct_count
    progress.time_spent_seconds += time_taken
    progress.calculate_accuracy()

    db.session.commit()
    flash('Technical Assessment submitted successfully!', 'success')
    return redirect(url_for('technical.result_view', result_id=result.id))


@technical_bp.route('/result/<int:result_id>')
@student_required
def result_view(result_id):
    result = TestResult.query.get_or_404(result_id)
    if result.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to result.', 'danger')
        return redirect(url_for('student.dashboard'))

    answers = result.get_answers()
    test = result.test
    questions = [tq.question for tq in test.test_questions]

    return render_template('technical/result.html', result=result, test=test, questions=questions, answers=answers)
