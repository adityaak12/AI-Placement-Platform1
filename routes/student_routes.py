from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.result import TestResult
from models.coding import CodingSubmission
from models.resume import ResumeAnalysis
from models.interview import InterviewSession
from models.recommendation import Recommendation
from models.progress import StudentProgress
from ai.performance_analysis import analyze_student_performance
from ai.recommendation_engine import generate_personalized_recommendations
from utils.decorators import student_required

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@student_required
def dashboard():
    # Fetch student history
    results = TestResult.query.filter_by(student_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    coding_subs = CodingSubmission.query.filter_by(student_id=current_user.id).order_by(CodingSubmission.submitted_at.desc()).all()
    resumes = ResumeAnalysis.query.filter_by(student_id=current_user.id).order_by(ResumeAnalysis.created_at.desc()).all()
    interviews = InterviewSession.query.filter_by(student_id=current_user.id).order_by(InterviewSession.created_at.desc()).all()

    # Compute AI Performance Profile
    perf = analyze_student_performance(current_user, results, coding_subs, resumes, interviews)

    # Generate / sync AI Recommendations
    recs = generate_personalized_recommendations(current_user, perf)

    return render_template(
        'student/dashboard.html',
        perf=perf,
        recommendations=recs,
        recent_results=results[:5],
        recent_coding=coding_subs[:5],
        latest_resume=resumes[0] if resumes else None,
        latest_interview=interviews[0] if interviews else None
    )


@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', '').strip()
        current_user.college = request.form.get('college', '').strip()
        current_user.degree = request.form.get('degree', '').strip()
        grad_year = request.form.get('graduation_year', '').strip()
        current_user.graduation_year = int(grad_year) if grad_year.isdigit() else current_user.graduation_year
        current_user.target_role = request.form.get('target_role', 'Software Engineer').strip()
        current_user.skills = request.form.get('skills', '').strip()
        current_user.bio = request.form.get('bio', '').strip()

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('student.profile'))
        except Exception:
            db.session.rollback()
            flash('Failed to update profile. Please try again.', 'danger')

    return render_template('student/profile.html', user=current_user)


@student_bp.route('/progress')
@student_required
def progress():
    results = TestResult.query.filter_by(student_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    coding_subs = CodingSubmission.query.filter_by(student_id=current_user.id).order_by(CodingSubmission.submitted_at.desc()).all()
    resumes = ResumeAnalysis.query.filter_by(student_id=current_user.id).order_by(ResumeAnalysis.created_at.desc()).all()
    interviews = InterviewSession.query.filter_by(student_id=current_user.id).order_by(InterviewSession.created_at.desc()).all()

    perf = analyze_student_performance(current_user, results, coding_subs, resumes, interviews)
    progress_records = StudentProgress.query.filter_by(student_id=current_user.id).all()

    return render_template(
        'student/progress.html',
        perf=perf,
        progress_records=progress_records,
        total_tests=len(results),
        total_coding=len(coding_subs)
    )


@student_bp.route('/results')
@student_required
def results():
    all_results = TestResult.query.filter_by(student_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    coding_subs = CodingSubmission.query.filter_by(student_id=current_user.id).order_by(CodingSubmission.submitted_at.desc()).all()
    return render_template('student/results.html', results=all_results, coding_submissions=coding_subs)
