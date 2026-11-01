import os
import uuid
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from flask_login import current_user
from extensions import db
from models.resume import ResumeAnalysis
from ai.resume_analyzer import extract_text_from_file, analyze_resume_content, ROLE_SKILL_PROFILES
from utils.helpers import allowed_file
from utils.decorators import student_required

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')


@resume_bp.route('/')
@student_required
def index():
    analyses = ResumeAnalysis.query.filter_by(
        student_id=current_user.id
    ).order_by(ResumeAnalysis.created_at.desc()).all()

    return render_template('resume/index.html', analyses=analyses)


@resume_bp.route('/upload', methods=['GET', 'POST'])
@student_required
def upload():
    roles = list(ROLE_SKILL_PROFILES.keys())

    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part in request.', 'warning')
            return redirect(request.url)

        file = request.files['resume']
        target_role = request.form.get('target_role', 'Software Engineer')

        if file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Unsupported file type. Please upload a PDF, DOCX, or TXT file.', 'danger')
            return redirect(request.url)

        # Ensure upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        original_filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{original_filename}"
        file_path = os.path.join(upload_folder, unique_name)
        file.save(file_path)

        # Extract text & analyze with AI
        extracted_text = extract_text_from_file(file_path)
        analysis_data = analyze_resume_content(extracted_text, target_role=target_role)

        # Persist analysis
        analysis = ResumeAnalysis(
            student_id=current_user.id,
            original_filename=original_filename,
            stored_filename=unique_name,
            target_role=target_role,
            ats_score=analysis_data['ats_score'],
            matched_skills_json=json.dumps(analysis_data['matched_skills']),
            missing_skills_json=json.dumps(analysis_data['missing_skills']),
            sections_detected_json=json.dumps(analysis_data['sections_detected']),
            feedback_json=json.dumps(analysis_data['feedback'])
        )
        db.session.add(analysis)
        db.session.commit()

        flash(f'Resume analyzed successfully! ATS Match Score: {analysis.ats_score}%.', 'success')
        return redirect(url_for('resume.analysis_view', analysis_id=analysis.id))

    return render_template('resume/upload.html', roles=roles)


@resume_bp.route('/analysis/<int:analysis_id>')
@student_required
def analysis_view(analysis_id):
    analysis = ResumeAnalysis.query.get_or_404(analysis_id)
    if analysis.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to resume analysis.', 'danger')
        return redirect(url_for('resume.index'))

    return render_template(
        'resume/analysis.html',
        analysis=analysis,
        feedback=analysis.get_feedback(),
        matched_skills=analysis.get_matched_skills(),
        missing_skills=analysis.get_missing_skills(),
        sections=analysis.get_sections()
    )
