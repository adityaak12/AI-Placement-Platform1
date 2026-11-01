import re

INTERVIEW_QUESTION_BANK = {
    'technical': [
        {
            'id': 1,
            'question': "Can you explain the four core principles of Object-Oriented Programming (OOP) and give a practical example of polymorphism?",
            'keywords': ['encapsulation', 'abstraction', 'inheritance', 'polymorphism', 'method overriding', 'interface', 'class'],
            'ideal_answer': "The four principles are Encapsulation (bundling data and methods), Abstraction (hiding implementation details), Inheritance (reusing existing class features), and Polymorphism (ability of an object to take many forms, e.g. method overriding where a subclass provides a specific implementation of a parent method)."
        },
        {
            'id': 2,
            'question': "What is the difference between a Process and a Thread? How does inter-process communication (IPC) work?",
            'keywords': ['memory', 'shared', 'address space', 'overhead', 'context switch', 'lightweight', 'pipe', 'message queue', 'shared memory'],
            'ideal_answer': "A process is an executing program with its own independent memory address space. A thread is a lightweight execution unit within a process that shares memory and resources with sibling threads. IPC is required for processes to exchange data using pipes, sockets, message queues, or shared memory."
        },
        {
            'id': 3,
            'question': "Explain the ACID properties in database transactions and why they are essential for enterprise applications.",
            'keywords': ['atomicity', 'consistency', 'isolation', 'durability', 'all or nothing', 'rollback', 'commit', 'concurrency'],
            'ideal_answer': "ACID stands for Atomicity (all operations succeed or roll back), Consistency (data moves from one valid state to another), Isolation (concurrent transactions execute independently without interference), and Durability (committed changes persist even during system crashes)."
        },
        {
            'id': 4,
            'question': "How does a Hash Table achieve average O(1) time complexity, and how do you handle hash collisions?",
            'keywords': ['hash function', 'collision', 'chaining', 'open addressing', 'linear probing', 'bucket', 'load factor', 'o(1)'],
            'ideal_answer': "A Hash Table maps keys to bucket indices using a hash function, allowing O(1) lookup. When multiple keys hash to the same bucket (collision), it is resolved using Separate Chaining (linked lists/trees at each bucket) or Open Addressing (linear or quadratic probing)."
        },
        {
            'id': 5,
            'question': "What is the difference between TCP and UDP protocols? In what campus recruitment scenario would you choose one over the other?",
            'keywords': ['tcp', 'udp', 'connection oriented', 'connectionless', 'handshake', 'reliable', 'packet loss', 'streaming', 'retransmission'],
            'ideal_answer': "TCP is connection-oriented and reliable, using a 3-way handshake and packet acknowledgments (ideal for web, banking, file transfer). UDP is connectionless and lightweight without retransmissions, offering higher speed (ideal for live video streaming and real-time multiplayer gaming)."
        }
    ],
    'hr': [
        {
            'id': 1,
            'question': "Tell me about yourself, your academic background, and why you are interested in a software engineering career.",
            'keywords': ['computer science', 'engineering', 'passion', 'projects', 'problem solving', 'technologies', 'learn', 'career'],
            'ideal_answer': "Structure your answer with: 1) Who you are & your educational background, 2) Technical domains you enjoy and key projects you have built, 3) Your passion for solving real-world problems and why you are eager to contribute to the company."
        },
        {
            'id': 2,
            'question': "Describe a challenging situation or conflict you encountered in a college team project. How did you resolve it?",
            'keywords': ['team', 'conflict', 'deadline', 'communication', 'role', 'resolution', 'agreed', 'outcome', 'learned'],
            'ideal_answer': "Use the STAR method: Situation (project context), Task (what was required), Action (active listening, open team discussion, redistributing workload), and Result (successful project delivery on time and improved collaboration)."
        },
        {
            'id': 3,
            'question': "What are your greatest technical strengths, and what is one area or weakness you are currently working to improve?",
            'keywords': ['strength', 'weakness', 'improvement', 'learning', 'consistency', 'curiosity', 'practice', 'action'],
            'ideal_answer': "Highlight a genuine strength backed by examples (e.g., algorithmic problem solving or rapid debugging) and a real weakness that you are proactively working to remedy (e.g., initial public speaking, which you are improving via presentations)."
        },
        {
            'id': 4,
            'question': "Where do you envision yourself professionally three to five years after joining our organization?",
            'keywords': ['growth', 'lead', 'architecture', 'mentor', 'impact', 'responsibility', 'skills', 'contribute'],
            'ideal_answer': "Focus on deepening technical expertise, mastering system architecture, taking ownership of high-impact features, and eventually mentoring junior team members while continuing to align with company goals."
        },
        {
            'id': 5,
            'question': "Why should our company hire you over other qualified candidates from your campus?",
            'keywords': ['value', 'adaptability', 'fast learner', 'work ethic', 'projects', 'passion', 'collaborate', 'commitment'],
            'ideal_answer': "Emphasize your combination of solid computer science fundamentals, hands-on project experience, rapid learning agility, and a strong collaborative work ethic aligned with the company culture."
        }
    ]
}


def get_questions_for_interview(interview_type='technical', count=5):
    """Returns a list of interview questions for the given type."""
    bank = INTERVIEW_QUESTION_BANK.get(interview_type.lower(), INTERVIEW_QUESTION_BANK['technical'])
    return bank[:count]


def evaluate_candidate_answer(question_obj, candidate_response):
    """
    Evaluates candidate's response using keyword matching, length metrics,
    clarity indicators, and provides targeted scoring and feedback.
    """
    clean_resp = candidate_response.strip().lower()
    words = clean_resp.split()
    word_count = len(words)

    if word_count < 5:
        return {
            'score': 20,
            'technical_depth': 20,
            'clarity': 30,
            'keywords_matched': [],
            'feedback': "Your answer is too brief. Provide detailed explanations and real-world examples.",
            'ideal_answer': question_obj.get('ideal_answer', '')
        }

    keywords = question_obj.get('keywords', [])
    matched_keywords = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', clean_resp)]
    keyword_coverage = len(matched_keywords) / max(len(keywords), 1)

    # 1. Depth & Keyword Match Score (0 - 50 pts)
    depth_score = min(keyword_coverage * 50, 50)

    # 2. Length & Completeness (0 - 30 pts)
    if word_count >= 50:
        length_score = 30
    elif word_count >= 25:
        length_score = 22
    else:
        length_score = 12

    # 3. Clarity & Structure (0 - 20 pts)
    # Check for sentence variety or structured indicators (because, for example, first, also, such as)
    struct_tokens = ['because', 'example', 'first', 'second', 'such as', 'furthermore', 'therefore']
    found_tokens = [tok for tok in struct_tokens if tok in clean_resp]
    clarity_score = min(12 + len(found_tokens) * 3, 20)

    total_score = min(round(depth_score + length_score + clarity_score, 1), 100)

    # Construct constructive feedback
    feedback_parts = []
    if len(matched_keywords) >= 3:
        feedback_parts.append(f"Good technical accuracy covering key concepts: {', '.join(matched_keywords[:3])}.")
    else:
        feedback_parts.append("Consider incorporating more standard technical terminology and specific examples.")

    if word_count < 30:
        feedback_parts.append("Elaborate further on implementation details or trade-offs.")
    else:
        feedback_parts.append("Good answer length and articulation.")

    return {
        'score': total_score,
        'technical_depth': round(min((depth_score / 50) * 100, 100), 1),
        'clarity': round(min((clarity_score / 20) * 100, 100), 1),
        'keywords_matched': matched_keywords,
        'feedback': " ".join(feedback_parts),
        'ideal_answer': question_obj.get('ideal_answer', '')
    }


def summarize_interview_session(evaluations, interview_type='technical'):
    """
    Summarizes all answered questions in an interview session,
    generating overall scores, key strengths, and an improvement plan.
    """
    if not evaluations:
        return {
            'overall_score': 0.0,
            'technical_score': 0.0,
            'communication_score': 0.0,
            'confidence_score': 0.0,
            'summary': "No responses recorded.",
            'strengths': [],
            'improvements': []
        }

    total_score = sum(e['score'] for e in evaluations) / len(evaluations)
    tech_score = sum(e.get('technical_depth', e['score']) for e in evaluations) / len(evaluations)
    comm_score = sum(e.get('clarity', e['score']) for e in evaluations) / len(evaluations)
    conf_score = min(round((tech_score * 0.5 + comm_score * 0.5), 1), 100)

    strengths = []
    improvements = []

    if total_score >= 75:
        strengths.append(f"Outstanding performance across {interview_type.upper()} questions.")
        strengths.append("Demonstrated solid conceptual clarity and articulate communication.")
    elif total_score >= 50:
        strengths.append("Satisfactory grasp of fundamental questions.")
        improvements.append("Deepen explanations with architectural trade-offs and concrete project examples.")
    else:
        improvements.append("Review foundational concepts and practice speaking answers aloud.")
        improvements.append("Use the STAR (Situation, Task, Action, Result) method for structured responses.")

    return {
        'overall_score': round(total_score, 1),
        'technical_score': round(tech_score, 1),
        'communication_score': round(comm_score, 1),
        'confidence_score': round(conf_score, 1),
        'summary': f"Completed {len(evaluations)} question {interview_type.upper()} round with an overall score of {round(total_score, 1)}%.",
        'strengths': strengths,
        'improvements': improvements
    }

