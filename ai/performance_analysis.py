from collections import defaultdict


def analyze_student_performance(student, test_results, coding_submissions, resume_analyses, interview_sessions):
    """
    Computes an end-to-end performance profile for a student:
    - Category & subcategory accuracy
    - Strengths and Weaknesses identification
    - Placement Readiness Score (0-100)
    - Radar/bar chart metrics for UI rendering
    """
    category_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'tests_count': 0, 'total_time': 0})

    for res in test_results:
        cat = res.category or 'general'
        category_stats[cat]['correct'] += (res.correct_answers or 0)
        category_stats[cat]['total'] += (res.total_questions or 0)
        category_stats[cat]['tests_count'] += 1
        category_stats[cat]['total_time'] += (res.time_taken_seconds or 0)

    # Process coding submissions
    total_coding = len(coding_submissions)
    accepted_coding = sum(1 for c in coding_submissions if c.status == 'Accepted')
    coding_accuracy = (accepted_coding / total_coding * 100) if total_coding > 0 else 0.0

    # Process resume scores
    latest_resume = resume_analyses[0] if resume_analyses else None
    resume_score = latest_resume.ats_score if latest_resume else 0.0

    # Process interview scores
    latest_interview = interview_sessions[0] if interview_sessions else None
    interview_score = latest_interview.overall_score if latest_interview else 0.0

    # Compute category breakdowns
    breakdown = {}
    strengths = []
    weaknesses = []
    moderate = []

    for cat, data in category_stats.items():
        acc = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0.0
        acc_round = round(acc, 1)
        breakdown[cat] = {
            'accuracy': acc_round,
            'attempted': data['total'],
            'correct': data['correct'],
            'tests_count': data['tests_count'],
            'avg_time_per_test': round(data['total_time'] / max(data['tests_count'], 1), 1)
        }

        label = cat.replace('_', ' ').title()
        if acc >= 75 and data['total'] >= 5:
            strengths.append(f"{label} (Accuracy: {acc_round}%)")
        elif acc < 50:
            weaknesses.append(f"{label} (Accuracy: {acc_round}%)")
        else:
            moderate.append(f"{label} (Accuracy: {acc_round}%)")

    # Coding check
    if total_coding >= 3 and coding_accuracy >= 70:
        strengths.append(f"Coding Challenges ({accepted_coding}/{total_coding} Solved)")
    elif total_coding > 0 and coding_accuracy < 50:
        weaknesses.append(f"Coding Challenges ({accepted_coding}/{total_coding} Accepted)")

    # Overall Placement Readiness Score (0-100)
    # Weights: Aptitude (25%), Technical (25%), Coding (25%), Interview & Resume (25%)
    apt_acc = breakdown.get('aptitude', {}).get('accuracy', 0.0)
    tech_acc = breakdown.get('technical', {}).get('accuracy', 0.0)
    mock_acc = breakdown.get('mock_test', {}).get('accuracy', 0.0)

    # If mock test exists, combine with apt/tech
    if mock_acc > 0:
        written_score = (apt_acc * 0.35 + tech_acc * 0.35 + mock_acc * 0.3)
    else:
        written_score = (apt_acc * 0.5 + tech_acc * 0.5) if (apt_acc or tech_acc) else 0.0

    soft_skills_score = (interview_score * 0.5 + resume_score * 0.5) if (interview_score or resume_score) else 0.0

    placement_readiness = round(
        (written_score * 0.40) +
        (coding_accuracy * 0.35) +
        (soft_skills_score * 0.25),
        1
    )

    # Readiness Tier
    if placement_readiness >= 75:
        readiness_badge = "Placement Ready"
        badge_class = "success"
    elif placement_readiness >= 50:
        readiness_badge = "Good Progress"
        badge_class = "primary"
    elif placement_readiness >= 25:
        readiness_badge = "Needs Practice"
        badge_class = "warning"
    else:
        readiness_badge = "Getting Started"
        badge_class = "secondary"

    return {
        'placement_readiness': placement_readiness,
        'readiness_badge': readiness_badge,
        'badge_class': badge_class,
        'breakdown': breakdown,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'moderate': moderate,
        'coding_accuracy': round(coding_accuracy, 1),
        'coding_solved': accepted_coding,
        'coding_total': total_coding,
        'resume_score': round(resume_score, 1),
        'interview_score': round(interview_score, 1),
        'chart_labels': ['Aptitude', 'Technical', 'Coding', 'Mock Tests', 'Interview', 'Resume'],
        'chart_values': [
            round(apt_acc, 1),
            round(tech_acc, 1),
            round(coding_accuracy, 1),
            round(mock_acc, 1),
            round(interview_score, 1),
            round(resume_score, 1)
        ]
    }

