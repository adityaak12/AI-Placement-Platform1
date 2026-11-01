from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from extensions import db
from models.recommendation import Recommendation
from models.result import TestResult
from models.coding import CodingSubmission
from models.resume import ResumeAnalysis
from models.interview import InterviewSession
from ai.performance_analysis import analyze_student_performance
from ai.recommendation_engine import generate_personalized_recommendations
from utils.decorators import student_required

recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/recommendations')


@recommendation_bp.route('/')
@student_required
def index():
    recs = Recommendation.query.filter_by(
        student_id=current_user.id
    ).order_by(Recommendation.is_completed.asc(), Recommendation.created_at.desc()).all()

    return render_template('recommendation/recommendations.html', recommendations=recs)


@recommendation_bp.route('/complete/<int:rec_id>', methods=['POST'])
@student_required
def complete_recommendation(rec_id):
    rec = Recommendation.query.get_or_404(rec_id)
    if rec.student_id == current_user.id:
        rec.is_completed = True
        db.session.commit()
        flash('Recommendation marked as completed!', 'success')
    return redirect(url_for('recommendation.index'))


@recommendation_bp.route('/refresh', methods=['POST'])
@student_required
def refresh_recommendations():
    results = TestResult.query.filter_by(student_id=current_user.id).all()
    coding_subs = CodingSubmission.query.filter_by(student_id=current_user.id).all()
    resumes = ResumeAnalysis.query.filter_by(student_id=current_user.id).order_by(ResumeAnalysis.created_at.desc()).all()
    interviews = InterviewSession.query.filter_by(student_id=current_user.id).order_by(InterviewSession.created_at.desc()).all()

    perf = analyze_student_performance(current_user, results, coding_subs, resumes, interviews)
    generate_personalized_recommendations(current_user, perf)

    flash('AI Recommendations refreshed based on your latest performance!', 'info')
    return redirect(url_for('recommendation.index'))

