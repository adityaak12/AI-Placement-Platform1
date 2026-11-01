from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import db
from models.user import User
from models.question import Question
from models.test import Test, TestQuestion
from models.result import TestResult
from models.coding import CodingProblem, CodingSubmission
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_questions = Question.query.count()
    total_tests = Test.query.count()
    total_results = TestResult.query.count()
    total_coding = CodingSubmission.query.count()

    recent_students = User.query.filter_by(role='student').order_by(User.created_at.desc()).limit(5).all()
    recent_results = TestResult.query.order_by(TestResult.completed_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_questions=total_questions,
        total_tests=total_tests,
        total_results=total_results,
        total_coding=total_coding,
        recent_students=recent_students,
        recent_results=recent_results
    )


@admin_bp.route('/students')
@admin_required
def students():
    student_list = User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    return render_template('admin/students.html', students=student_list)


@admin_bp.route('/questions', methods=['GET', 'POST'])
@admin_required
def questions():
    if request.method == 'POST':
        q_text = request.form.get('question_text', '').strip()
        opt_a = request.form.get('option_a', '').strip()
        opt_b = request.form.get('option_b', '').strip()
        opt_c = request.form.get('option_c', '').strip()
        opt_d = request.form.get('option_d', '').strip()
        correct = request.form.get('correct_option', '').strip().upper()
        category = request.form.get('category', 'aptitude').strip().lower()
        subcategory = request.form.get('subcategory', 'general').strip().lower()
        difficulty = request.form.get('difficulty', 'medium').strip().lower()
        explanation = request.form.get('explanation', '').strip()

        if not q_text or not opt_a or not opt_b or not opt_c or not opt_d or not correct:
            flash('Please fill in all required question and option fields.', 'warning')
        else:
            q = Question(
                question_text=q_text,
                option_a=opt_a,
                option_b=opt_b,
                option_c=opt_c,
                option_d=opt_d,
                correct_option=correct,
                category=category,
                subcategory=subcategory,
                difficulty=difficulty,
                explanation=explanation
            )
            db.session.add(q)
            db.session.commit()
            flash('New question successfully added!', 'success')
            return redirect(url_for('admin.questions'))

    cat_filter = request.args.get('category', 'all')
    query = Question.query
    if cat_filter != 'all':
        query = query.filter_by(category=cat_filter)

    all_questions = query.order_by(Question.id.desc()).all()
    return render_template('admin/questions.html', questions=all_questions, selected_cat=cat_filter)


@admin_bp.route('/questions/delete/<int:q_id>', methods=['POST'])
@admin_required
def delete_question(q_id):
    q = Question.query.get_or_404(q_id)
    db.session.delete(q)
    db.session.commit()
    flash('Question deleted successfully.', 'info')
    return redirect(url_for('admin.questions'))


@admin_bp.route('/tests', methods=['GET', 'POST'])
@admin_required
def tests():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'aptitude').strip().lower()
        subcategory = request.form.get('subcategory', '').strip().lower()
        duration = int(request.form.get('duration_minutes', 30))
        total_marks = int(request.form.get('total_marks', 100))
        passing_marks = int(request.form.get('passing_marks', 40))

        if not title:
            flash('Test title is required.', 'warning')
        else:
            new_test = Test(
                title=title,
                description=description,
                category=category,
                subcategory=subcategory,
                duration_minutes=duration,
                total_marks=total_marks,
                passing_marks=passing_marks,
                is_active=True
            )
            db.session.add(new_test)
            db.session.commit()
            flash('New test created successfully!', 'success')
            return redirect(url_for('admin.tests'))

    all_tests = Test.query.order_by(Test.id.desc()).all()
    return render_template('admin/tests.html', tests=all_tests)


@admin_bp.route('/tests/toggle/<int:test_id>', methods=['POST'])
@admin_required
def toggle_test(test_id):
    t = Test.query.get_or_404(test_id)
    t.is_active = not t.is_active
    db.session.commit()
    flash(f"Test '{t.title}' is now {'Active' if t.is_active else 'Inactive'}.", 'info')
    return redirect(url_for('admin.tests'))


@admin_bp.route('/results')
@admin_required
def results():
    all_results = TestResult.query.order_by(TestResult.completed_at.desc()).all()
    return render_template('admin/results.html', results=all_results)


@admin_bp.route('/categories')
@admin_required
def categories():
    categories_data = [
        {'name': 'Aptitude - Quantitative', 'type': 'aptitude', 'sub': 'quantitative', 'count': Question.query.filter_by(category='aptitude', subcategory='quantitative').count()},
        {'name': 'Aptitude - Logical Reasoning', 'type': 'aptitude', 'sub': 'logical', 'count': Question.query.filter_by(category='aptitude', subcategory='logical').count()},
        {'name': 'Aptitude - Verbal Ability', 'type': 'aptitude', 'sub': 'verbal', 'count': Question.query.filter_by(category='aptitude', subcategory='verbal').count()},
        {'name': 'Technical - Data Structures & Algorithms', 'type': 'technical', 'sub': 'dsa', 'count': Question.query.filter_by(category='technical', subcategory='dsa').count()},
        {'name': 'Technical - Database Management Systems', 'type': 'technical', 'sub': 'dbms', 'count': Question.query.filter_by(category='technical', subcategory='dbms').count()},
        {'name': 'Technical - Operating Systems', 'type': 'technical', 'sub': 'os', 'count': Question.query.filter_by(category='technical', subcategory='os').count()},
        {'name': 'Technical - Computer Networks', 'type': 'technical', 'sub': 'cn', 'count': Question.query.filter_by(category='technical', subcategory='cn').count()},
        {'name': 'Technical - Programming Fundamentals', 'type': 'technical', 'sub': 'programming', 'count': Question.query.filter_by(category='technical', subcategory='programming').count()},
    ]
    return render_template('admin/categories.html', categories=categories_data)

