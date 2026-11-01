import time
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user
from extensions import db
from models.coding import CodingProblem, CodingSubmission
from utils.code_runner import execute_python_code
from utils.decorators import student_required

coding_bp = Blueprint('coding', __name__, url_prefix='/coding')


@coding_bp.route('/')
@student_required
def index():
    diff = request.args.get('difficulty', 'all')
    cat = request.args.get('category', 'all')

    query = CodingProblem.query
    if diff != 'all':
        query = query.filter_by(difficulty=diff)
    if cat != 'all':
        query = query.filter_by(category=cat)

    problems = query.order_by(CodingProblem.id.asc()).all()

    # User's solved problems
    user_solved_ids = {
        sub.problem_id for sub in CodingSubmission.query.filter_by(
            student_id=current_user.id,
            status='Accepted'
        ).all()
    }

    return render_template(
        'coding/index.html',
        problems=problems,
        user_solved_ids=user_solved_ids,
        selected_diff=diff,
        selected_cat=cat
    )


@coding_bp.route('/problem/<slug>')
@student_required
def problem_detail(slug):
    problem = CodingProblem.query.filter_by(slug=slug).first_or_404()
    recent_submissions = CodingSubmission.query.filter_by(
        student_id=current_user.id,
        problem_id=problem.id
    ).order_by(CodingSubmission.submitted_at.desc()).limit(5).all()

    last_code = recent_submissions[0].code if recent_submissions else problem.starter_code

    return render_template(
        'coding/problem.html',
        problem=problem,
        recent_submissions=recent_submissions,
        code=last_code
    )


@coding_bp.route('/run/<slug>', methods=['POST'])
@student_required
def run_code(slug):
    problem = CodingProblem.query.filter_by(slug=slug).first_or_404()
    data = request.get_json() or {}
    code = data.get('code', '')

    if not code.strip():
        return jsonify({'status': 'Error', 'error': 'Code is empty'}), 400

    # Only run against sample (non-hidden) test cases
    sample_tests = [tc for tc in problem.get_test_cases() if not tc.get('is_hidden', False)]
    if not sample_tests:
        sample_tests = problem.get_test_cases()[:2]

    exec_res = execute_python_code(code, sample_tests)
    return jsonify(exec_res)


@coding_bp.route('/submit/<slug>', methods=['POST'])
@student_required
def submit_code(slug):
    problem = CodingProblem.query.filter_by(slug=slug).first_or_404()
    code = request.form.get('code', '').strip()
    language = request.form.get('language', 'python')

    if not code:
        flash('Please enter your code before submitting.', 'warning')
        return redirect(url_for('coding.problem_detail', slug=slug))

    test_cases = problem.get_test_cases()
    exec_res = execute_python_code(code, test_cases)

    # Compute score (100 * passed / total)
    total_tc = max(exec_res.get('total', 1), 1)
    passed_tc = exec_res.get('passed', 0)
    score = round((passed_tc / total_tc) * 100.0, 1)

    sub = CodingSubmission(
        student_id=current_user.id,
        problem_id=problem.id,
        code=code,
        language=language,
        status=exec_res.get('status', 'Wrong Answer'),
        passed_tests=passed_tc,
        total_tests=total_tc,
        score=score,
        execution_time_ms=exec_res.get('execution_time_ms', 0.0),
        error_message=exec_res.get('error')
    )
    db.session.add(sub)
    db.session.commit()

    if exec_res.get('status') == 'Accepted':
        flash('Congratulations! All test cases passed with Accepted status.', 'success')
    else:
        flash(f'Submission completed: {passed_tc}/{total_tc} test cases passed ({exec_res.get("status")}).', 'warning')

    return redirect(url_for('coding.submission_result', submission_id=sub.id))


@coding_bp.route('/result/<int:submission_id>')
@student_required
def submission_result(submission_id):
    sub = CodingSubmission.query.get_or_404(submission_id)
    if sub.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to submission.', 'danger')
        return redirect(url_for('coding.index'))

    return render_template('coding/result.html', submission=sub, problem=sub.problem)

