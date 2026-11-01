from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user
from extensions import db
from models.interview import InterviewSession
from ai.mock_interview import (
    get_questions_for_interview,
    evaluate_candidate_answer,
    summarize_interview_session
)
from utils.decorators import student_required

interview_bp = Blueprint('interview', __name__, url_prefix='/interview')


@interview_bp.route('/')
@student_required
def index():
    past_sessions = InterviewSession.query.filter_by(
        student_id=current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

    return render_template('interview/index.html', past_sessions=past_sessions)


@interview_bp.route('/start', methods=['POST'])
@student_required
def start_interview():
    interview_type = request.form.get('interview_type', 'technical').lower()
    target_role = request.form.get('target_role', current_user.target_role or 'Software Engineer')

    questions = get_questions_for_interview(interview_type, count=5)
    first_q = questions[0]['question'] if questions else "Tell me about yourself."

    session = InterviewSession(
        student_id=current_user.id,
        interview_type=interview_type,
        target_role=target_role,
        status='in_progress',
        current_question_index=0
    )
    session.append_message('interviewer', first_q)
    db.session.add(session)
    db.session.commit()

    if interview_type == 'hr':
        return redirect(url_for('interview.hr_interview', session_id=session.id))
    return redirect(url_for('interview.technical_interview', session_id=session.id))


@interview_bp.route('/technical/<int:session_id>')
@student_required
def technical_interview(session_id):
    session = InterviewSession.query.get_or_404(session_id)
    if session.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to interview session.', 'danger')
        return redirect(url_for('interview.index'))

    if session.status == 'completed':
        return redirect(url_for('interview.feedback_view', session_id=session.id))

    questions = get_questions_for_interview('technical', count=5)
    curr_idx = session.current_question_index
    curr_q = questions[curr_idx] if curr_idx < len(questions) else None

    return render_template(
        'interview/technical.html',
        session=session,
        current_question=curr_q,
        question_num=curr_idx + 1,
        total_questions=len(questions),
        messages=session.get_messages()
    )


@interview_bp.route('/hr/<int:session_id>')
@student_required
def hr_interview(session_id):
    session = InterviewSession.query.get_or_404(session_id)
    if session.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to interview session.', 'danger')
        return redirect(url_for('interview.index'))

    if session.status == 'completed':
        return redirect(url_for('interview.feedback_view', session_id=session.id))

    questions = get_questions_for_interview('hr', count=5)
    curr_idx = session.current_question_index
    curr_q = questions[curr_idx] if curr_idx < len(questions) else None

    return render_template(
        'interview/hr.html',
        session=session,
        current_question=curr_q,
        question_num=curr_idx + 1,
        total_questions=len(questions),
        messages=session.get_messages()
    )


@interview_bp.route('/answer/<int:session_id>', methods=['POST'])
@student_required
def submit_answer(session_id):
    session = InterviewSession.query.get_or_404(session_id)
    if session.student_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    candidate_answer = request.form.get('answer', '').strip()
    if not candidate_answer:
        flash('Please enter an answer before continuing.', 'warning')
        endpoint = 'interview.hr_interview' if session.interview_type == 'hr' else 'interview.technical_interview'
        return redirect(url_for(endpoint, session_id=session.id))

    questions = get_questions_for_interview(session.interview_type, count=5)
    curr_idx = session.current_question_index

    if curr_idx < len(questions):
        question_obj = questions[curr_idx]
        eval_result = evaluate_candidate_answer(question_obj, candidate_answer)
    else:
        eval_result = {'score': 70.0, 'feedback': 'Answer recorded.', 'technical_depth': 70.0, 'clarity': 70.0}

    # Record candidate message with feedback
    session.append_message('candidate', candidate_answer, feedback=eval_result)

    # Move to next question or complete
    next_idx = curr_idx + 1
    session.current_question_index = next_idx

    if next_idx < len(questions):
        next_q_text = questions[next_idx]['question']
        session.append_message('interviewer', next_q_text)
        db.session.commit()
        endpoint = 'interview.hr_interview' if session.interview_type == 'hr' else 'interview.technical_interview'
        return redirect(url_for(endpoint, session_id=session.id))
    else:
        # Finalize interview session
        all_evals = []
        for msg in session.get_messages():
            if msg.get('role') == 'candidate' and 'feedback' in msg:
                all_evals.append(msg['feedback'])

        summary = summarize_interview_session(all_evals, interview_type=session.interview_type)
        session.status = 'completed'
        session.overall_score = summary['overall_score']
        session.technical_score = summary['technical_score']
        session.communication_score = summary['communication_score']
        session.confidence_score = summary['confidence_score']
        session.set_feedback(summary)
        session.completed_at = datetime.utcnow()
        db.session.commit()

        flash(f'Mock Interview completed! Your overall score: {session.overall_score}%.', 'success')
        return redirect(url_for('interview.feedback_view', session_id=session.id))


@interview_bp.route('/feedback/<int:session_id>')
@student_required
def feedback_view(session_id):
    session = InterviewSession.query.get_or_404(session_id)
    if session.student_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to interview feedback.', 'danger')
        return redirect(url_for('interview.index'))

    return render_template(
        'interview/feedback.html',
        session=session,
        feedback=session.get_feedback(),
        messages=session.get_messages()
    )

