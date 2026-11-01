from extensions import db
from models.recommendation import Recommendation


def generate_personalized_recommendations(student, performance_profile):
    """
    Evaluates performance profile metrics and dynamically generates
    prioritized, actionable placement recommendations for the student.
    """
    recommendations_to_add = []
    student_id = student.id

    breakdown = performance_profile.get('breakdown', {})
    apt_acc = breakdown.get('aptitude', {}).get('accuracy', 0.0)
    apt_count = breakdown.get('aptitude', {}).get('tests_count', 0)

    tech_acc = breakdown.get('technical', {}).get('accuracy', 0.0)
    tech_count = breakdown.get('technical', {}).get('tests_count', 0)

    mock_count = breakdown.get('mock_test', {}).get('tests_count', 0)
    mock_acc = breakdown.get('mock_test', {}).get('accuracy', 0.0)

    coding_solved = performance_profile.get('coding_solved', 0)
    coding_acc = performance_profile.get('coding_accuracy', 0.0)

    resume_score = performance_profile.get('resume_score', 0.0)
    interview_score = performance_profile.get('interview_score', 0.0)

    # 1. Aptitude Assessment Recommendation
    if apt_count == 0:
        recommendations_to_add.append({
            'recommendation_type': 'practice',
            'title': 'Start Aptitude Practice',
            'description': 'Campus placement screening rounds typically have a mandatory 60%+ aptitude cutoff.',
            'reason': 'No aptitude practice tests attempted yet.',
            'suggested_action': 'Solve 10 practice questions on Quantitative & Logical Reasoning.',
            'action_url': '/aptitude/practice',
            'priority': 'high'
        })
    elif apt_acc < 60.0:
        recommendations_to_add.append({
            'recommendation_type': 'practice',
            'title': 'Strengthen Quantitative & Reasoning Accuracy',
            'description': f'Your current aptitude accuracy is {apt_acc}%, which is below the common placement threshold.',
            'reason': f'Low aptitude accuracy ({apt_acc}%).',
            'suggested_action': 'Focus on Time & Work, Speed-Distance, and Series completion practice sets.',
            'action_url': '/aptitude/practice',
            'priority': 'high'
        })

    # 2. Technical Knowledge Recommendation
    if tech_count == 0:
        recommendations_to_add.append({
            'recommendation_type': 'practice',
            'title': 'Test Core CS Fundamentals',
            'description': 'Revise Core Computer Science concepts including DBMS, OS, Computer Networks, and OOP.',
            'reason': 'No technical practice recorded.',
            'suggested_action': 'Complete a 15-minute technical quiz.',
            'action_url': '/technical/practice',
            'priority': 'medium'
        })
    elif tech_acc < 65.0:
        recommendations_to_add.append({
            'recommendation_type': 'practice',
            'title': 'Revise Database & OS Concepts',
            'description': f'Your technical accuracy is {tech_acc}%. Campus technical rounds rigorously test ACID properties and process scheduling.',
            'reason': f'Technical score ({tech_acc}%) needs reinforcement.',
            'suggested_action': 'Practice DBMS queries and OS threading questions.',
            'action_url': '/technical/practice',
            'priority': 'high'
        })

    # 3. Coding Challenge Recommendation
    if coding_solved < 3:
        recommendations_to_add.append({
            'recommendation_type': 'coding',
            'title': 'Solve Placement Coding Problems',
            'description': 'Top product and service companies require solving 1-2 coding questions within 45 minutes.',
            'reason': f'Only {coding_solved} coding challenges solved so far.',
            'suggested_action': 'Solve Easy to Medium problems in Arrays, Strings, and Two Pointers.',
            'action_url': '/coding',
            'priority': 'high'
        })
    elif coding_acc < 60.0:
        recommendations_to_add.append({
            'recommendation_type': 'coding',
            'title': 'Improve Coding Test Case Pass Rate',
            'description': f'Your coding submission success rate is {coding_acc}%. Pay attention to edge cases and boundary constraints.',
            'reason': 'Multiple submissions encountered wrong answers or runtime errors.',
            'suggested_action': 'Refactor failed submissions and review time complexity.',
            'action_url': '/coding',
            'priority': 'medium'
        })

    # 4. Mock Test Recommendation
    if mock_count == 0:
        recommendations_to_add.append({
            'recommendation_type': 'mock_test',
            'title': 'Simulate Real Campus Mock Test',
            'description': 'Experience the pressure of real placement rounds with a timed full-length assessment.',
            'reason': 'No full mock tests completed.',
            'suggested_action': 'Take a 30-minute placement simulation test.',
            'action_url': '/mock-test',
            'priority': 'medium'
        })

    # 5. Resume Optimization Recommendation
    if resume_score == 0.0:
        recommendations_to_add.append({
            'recommendation_type': 'resume',
            'title': 'Upload & Analyze Resume with AI',
            'description': 'Get immediate ATS compatibility scoring, missing skills breakdown, and formatting advice.',
            'reason': 'Resume has not been uploaded yet.',
            'suggested_action': 'Upload your resume (PDF/DOCX) in the Resume Analyzer module.',
            'action_url': '/resume/upload',
            'priority': 'high'
        })
    elif resume_score < 75.0:
        recommendations_to_add.append({
            'recommendation_type': 'resume',
            'title': 'Enhance Resume ATS Score',
            'description': f'Your current ATS resume score is {resume_score}%. Incorporate missing keywords and quantified project results.',
            'reason': f'Resume ATS score ({resume_score}%) can be improved.',
            'suggested_action': 'Review the missing skills list and update your resume.',
            'action_url': '/resume/analysis',
            'priority': 'medium'
        })

    # 6. Mock Interview Recommendation
    if interview_score == 0.0:
        recommendations_to_add.append({
            'recommendation_type': 'interview',
            'title': 'Prepare with AI Mock Interviews',
            'description': 'Practice HR and Technical round questions with real-time AI feedback on your communication and answers.',
            'reason': 'No mock interview sessions completed.',
            'suggested_action': 'Start a 5-question Technical or HR interview simulation.',
            'action_url': '/interview',
            'priority': 'medium'
        })

    # Sync into database: clear old uncompleted recommendations and save new
    try:
        Recommendation.query.filter_by(student_id=student_id, is_completed=False).delete()
        for rec in recommendations_to_add[:5]:  # Top 5 prioritized recommendations
            rec_obj = Recommendation(
                student_id=student_id,
                recommendation_type=rec['recommendation_type'],
                title=rec['title'],
                description=rec['description'],
                reason=rec.get('reason'),
                suggested_action=rec.get('suggested_action'),
                action_url=rec.get('action_url'),
                priority=rec.get('priority', 'medium'),
                is_completed=False
            )
            db.session.add(rec_obj)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return recommendations_to_add

