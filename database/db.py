import json
from extensions import db
from models.user import User
from models.question import Question
from models.test import Test, TestQuestion
from models.coding import CodingProblem, CodingSubmission
from models.result import TestResult
from models.progress import StudentProgress
from models.recommendation import Recommendation


def init_db(app):
    """Initializes tables and populates seed data if database is new."""
    with app.app_context():
        db.create_all()
        seed_data()


def seed_data():
    """Seeds essential users, questions, coding problems, tests, and demo metrics."""
    if User.query.first():
        return  # Database already seeded

    # 1. Seed Users (Admin and Demo Student)
    admin = User(
        name='Admin Officer',
        email='admin@placement.edu',
        role='admin',
        college='Campus Placement Cell',
        degree='Administration',
        graduation_year=2024,
        target_role='Placement Administrator',
        skills='Administration, Campus Recruitment, Analytics',
        bio='Lead Placement Coordinator managing student performance, tests, and training modules.'
    )
    admin.set_password('Admin@123')
    db.session.add(admin)

    student = User(
        name='Aditya Madne',
        email='student@placement.edu',
        role='student',
        college='Government College of Engineering',
        degree='B.Tech in Computer Science',
        graduation_year=2026,
        target_role='Software Engineer',
        skills='Python, Java, C++, SQL, HTML, CSS, JavaScript, React, Git',
        bio='Final year engineering student preparing for campus recruitment drives at product & tech service firms.'
    )
    student.set_password('Student@123')
    db.session.add(student)
    db.session.commit()

    # 2. Seed Questions (Aptitude & Technical)
    sample_questions = [
        # Aptitude - Quantitative
        {
            'question_text': 'A and B together can complete a work in 12 days, while B alone can finish it in 30 days. In how many days can A alone finish the work?',
            'option_a': '18 days',
            'option_b': '20 days',
            'option_c': '24 days',
            'option_d': '15 days',
            'correct_option': 'B',
            'category': 'aptitude',
            'subcategory': 'quantitative',
            'difficulty': 'medium',
            'explanation': '1/A = 1/12 - 1/30 = (5 - 2)/60 = 3/60 = 1/20. Hence, A alone takes 20 days.'
        },
        {
            'question_text': 'A train 240 m long passes a pole in 24 seconds. How long will it take to pass a platform 650 m long?',
            'option_a': '65 seconds',
            'option_b': '89 seconds',
            'option_c': '100 seconds',
            'option_d': '75 seconds',
            'correct_option': 'B',
            'category': 'aptitude',
            'subcategory': 'quantitative',
            'difficulty': 'medium',
            'explanation': 'Speed = 240 / 24 = 10 m/s. Total distance to pass platform = 240 + 650 = 890 m. Time = 890 / 10 = 89 seconds.'
        },
        {
            'question_text': 'What is 15% of 40% of 2500?',
            'option_a': '150',
            'option_b': '125',
            'option_c': '175',
            'option_d': '100',
            'correct_option': 'A',
            'category': 'aptitude',
            'subcategory': 'quantitative',
            'difficulty': 'easy',
            'explanation': '40% of 2500 = 1000. 15% of 1000 = 150.'
        },
        {
            'question_text': 'A shopkeeper sells an article for $840 at a gain of 20%. What was the cost price?',
            'option_a': '$700',
            'option_b': '$720',
            'option_c': '$680',
            'option_d': '$710',
            'correct_option': 'A',
            'category': 'aptitude',
            'subcategory': 'quantitative',
            'difficulty': 'easy',
            'explanation': 'CP = (SP * 100) / (100 + Gain%) = (840 * 100) / 120 = 700.'
        },

        # Aptitude - Logical Reasoning
        {
            'question_text': 'Find the next number in the series: 3, 7, 15, 31, 63, ?',
            'option_a': '127',
            'option_b': '126',
            'option_c': '128',
            'option_d': '125',
            'correct_option': 'A',
            'category': 'aptitude',
            'subcategory': 'logical',
            'difficulty': 'easy',
            'explanation': 'The pattern is (x * 2) + 1. (63 * 2) + 1 = 127.'
        },
        {
            'question_text': 'Pointing to a photograph of a boy, Suresh said, "He is the son of the only son of my mother." How is Suresh related to that boy?',
            'option_a': 'Brother',
            'option_b': 'Uncle',
            'option_c': 'Father',
            'option_d': 'Cousin',
            'correct_option': 'C',
            'category': 'aptitude',
            'subcategory': 'logical',
            'difficulty': 'medium',
            'explanation': 'The only son of Suresh\'s mother is Suresh himself. Therefore, the boy is Suresh\'s son, making Suresh the father.'
        },
        {
            'question_text': 'If in a certain code, COMPUTER is written as RFUVQNPC, how is MEDICINE written in that code?',
            'option_a': 'EOJDJEFM',
            'option_b': 'EOJDEJFM',
            'option_c': 'MFEJDJOE',
            'option_d': 'EOJDJFEM',
            'correct_option': 'A',
            'category': 'aptitude',
            'subcategory': 'logical',
            'difficulty': 'hard',
            'explanation': 'Reverse the letters and shift each letter by +1, keeping the first and last letters swapped.'
        },

        # Aptitude - Verbal Ability
        {
            'question_text': 'Choose the word that is nearest in meaning (Synonym) to CANDID:',
            'option_a': 'Deceptive',
            'option_b': 'Frank',
            'option_c': 'Arrogant',
            'option_d': 'Reserved',
            'correct_option': 'B',
            'category': 'aptitude',
            'subcategory': 'verbal',
            'difficulty': 'easy',
            'explanation': 'Candid means truthful, straightforward, and frank.'
        },
        {
            'question_text': 'Find the correctly spelt word:',
            'option_a': 'Accomodation',
            'option_b': 'Accommodation',
            'option_c': 'Acommodation',
            'option_d': 'Accomadation',
            'correct_option': 'B',
            'category': 'aptitude',
            'subcategory': 'verbal',
            'difficulty': 'easy',
            'explanation': 'The correct spelling is "Accommodation" with double c and double m.'
        },
        {
            'question_text': 'Fill in the blank: The manager insisted _______ inspecting the factory floors personally.',
            'option_a': 'on',
            'option_b': 'in',
            'option_c': 'at',
            'option_d': 'with',
            'correct_option': 'A',
            'category': 'aptitude',
            'subcategory': 'verbal',
            'difficulty': 'easy',
            'explanation': 'The verb "insist" takes the preposition "on".'
        },

        # Technical - Data Structures & Algorithms
        {
            'question_text': 'What is the worst-case time complexity of QuickSort when the pivot is poorly chosen?',
            'option_a': 'O(N log N)',
            'option_b': 'O(N)',
            'option_c': 'O(N^2)',
            'option_d': 'O(log N)',
            'correct_option': 'C',
            'category': 'technical',
            'subcategory': 'dsa',
            'difficulty': 'medium',
            'explanation': 'In the worst case (e.g. already sorted array with extreme element as pivot), QuickSort degrades to O(N^2).'
        },
        {
            'question_text': 'Which data structure is primarily used to implement Breadth-First Search (BFS) on a graph?',
            'option_a': 'Stack',
            'option_b': 'Queue',
            'option_c': 'Priority Queue',
            'option_d': 'Binary Search Tree',
            'correct_option': 'B',
            'category': 'technical',
            'subcategory': 'dsa',
            'difficulty': 'easy',
            'explanation': 'BFS visits neighbor nodes level-by-level using a FIFO Queue.'
        },
        {
            'question_text': 'What is the minimum number of queues needed to implement a Stack?',
            'option_a': '1',
            'option_b': '2',
            'option_c': '3',
            'option_d': 'Cannot be done',
            'correct_option': 'B',
            'category': 'technical',
            'subcategory': 'dsa',
            'difficulty': 'medium',
            'explanation': 'Two queues are standard to implement LIFO stack behavior (or one queue with recursive rotation).'
        },

        # Technical - DBMS
        {
            'question_text': 'Which normal form eliminates partial functional dependency on the primary key?',
            'option_a': 'First Normal Form (1NF)',
            'option_b': 'Second Normal Form (2NF)',
            'option_c': 'Third Normal Form (3NF)',
            'option_d': 'Boyce-Codd Normal Form (BCNF)',
            'correct_option': 'B',
            'category': 'technical',
            'subcategory': 'dbms',
            'difficulty': 'medium',
            'explanation': '2NF requires the table to be in 1NF and have all non-key attributes fully functionally dependent on the primary key.'
        },
        {
            'question_text': 'In SQL, which clause is used to filter aggregated grouped results?',
            'option_a': 'WHERE',
            'option_b': 'HAVING',
            'option_c': 'ORDER BY',
            'option_d': 'GROUP FILTER',
            'correct_option': 'B',
            'category': 'technical',
            'subcategory': 'dbms',
            'difficulty': 'easy',
            'explanation': 'The HAVING clause was added to SQL because the WHERE keyword cannot be used with aggregate functions.'
        },

        # Technical - Operating Systems
        {
            'question_text': 'Which of the following is NOT one of the four Coffman conditions required for a Deadlock to occur?',
            'option_a': 'Mutual Exclusion',
            'option_b': 'Hold and Wait',
            'option_c': 'Preemption Allowed',
            'option_d': 'Circular Wait',
            'correct_option': 'C',
            'category': 'technical',
            'subcategory': 'os',
            'difficulty': 'medium',
            'explanation': 'The condition is "No Preemption". If preemption is allowed, deadlocks cannot occur.'
        },
        {
            'question_text': 'What is the phenomenon where page fault rate increases even when increasing the number of page frames allocated to a process in FIFO page replacement?',
            'option_a': 'Thrashing',
            'option_b': 'Belady\'s Anomaly',
            'option_c': 'Convoy Effect',
            'option_d': 'Fragmentation',
            'correct_option': 'B',
            'category': 'technical',
            'subcategory': 'os',
            'difficulty': 'hard',
            'explanation': 'Belady\'s Anomaly is a counter-intuitive observation in FIFO page replacement where more frames result in more page faults.'
        },

        # Technical - Computer Networks
        {
            'question_text': 'At which OSI model layer does the IP (Internet Protocol) operate?',
            'option_a': 'Data Link Layer',
            'option_b': 'Transport Layer',
            'option_c': 'Network Layer',
            'option_d': 'Session Layer',
            'correct_option': 'C',
            'category': 'technical',
            'subcategory': 'cn',
            'difficulty': 'easy',
            'explanation': 'The Network Layer (Layer 3) handles routing, packet forwarding, and logical addressing using IP.'
        }
    ]

    created_questions = []
    for q_data in sample_questions:
        q = Question(**q_data)
        db.session.add(q)
        created_questions.append(q)
    db.session.commit()

    # 3. Seed Placement Tests
    apt_test = Test(
        title='Quantitative & Logical Aptitude Practice Test',
        description='Comprehensive 10-question placement screening assessment covering percentages, time-work, speed, and syllogisms.',
        category='aptitude',
        subcategory='general_aptitude',
        duration_minutes=15,
        total_marks=50,
        passing_marks=25,
        is_active=True
    )
    db.session.add(apt_test)

    tech_test = Test(
        title='Core CS Fundamentals Placement Test',
        description='Essential technical assessment covering Data Structures, Algorithms, DBMS, Operating Systems, and Networks.',
        category='technical',
        subcategory='core_cs',
        duration_minutes=20,
        total_marks=50,
        passing_marks=30,
        is_active=True
    )
    db.session.add(tech_test)

    mock_test = Test(
        title='Full Campus Placement Mock Assessment (TCS / Infosys Pattern)',
        description='Standard full-length campus recruitment mock test combining Quantitative, Logical, Verbal, and Technical CS questions.',
        category='mock_test',
        subcategory='placement_simulation',
        duration_minutes=30,
        total_marks=100,
        passing_marks=60,
        is_active=True
    )
    db.session.add(mock_test)
    db.session.commit()

    # Link questions to tests
    apt_questions = [q for q in created_questions if q.category == 'aptitude']
    tech_questions = [q for q in created_questions if q.category == 'technical']

    for i, q in enumerate(apt_questions):
        db.session.add(TestQuestion(test_id=apt_test.id, question_id=q.id, order_num=i+1, marks=5))

    for i, q in enumerate(tech_questions):
        db.session.add(TestQuestion(test_id=tech_test.id, question_id=q.id, order_num=i+1, marks=5))

    for i, q in enumerate(created_questions[:10]):
        db.session.add(TestQuestion(test_id=mock_test.id, question_id=q.id, order_num=i+1, marks=10))

    db.session.commit()

    # 4. Seed Coding Problems
    coding_problems = [
        {
            'title': 'Two Sum',
            'slug': 'two-sum',
            'difficulty': 'easy',
            'category': 'Arrays',
            'description': 'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou can print the two indices separated by a space.',
            'input_format': 'First line contains space-separated integers for the array.\nSecond line contains integer target.',
            'output_format': 'Print two 0-based indices separated by space in ascending order.',
            'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9',
            'sample_input': '2 7 11 15\n9',
            'sample_output': '0 1',
            'starter_code': 'import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    if not lines: return\n    nums = list(map(int, lines[0].split()))\n    target = int(lines[1])\n    \n    # Write logic here\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            print(f"{seen[diff]} {i}")\n            return\n        seen[num] = i\n\nif __name__ == "__main__":\n    solve()\n',
            'test_cases': [
                {'input': '2 7 11 15\n9', 'expected': '0 1', 'is_hidden': False},
                {'input': '3 2 4\n6', 'expected': '1 2', 'is_hidden': False},
                {'input': '3 3\n6', 'expected': '0 1', 'is_hidden': True},
                {'input': '1 5 8 10 14\n22', 'expected': '2 4', 'is_hidden': True}
            ]
        },
        {
            'title': 'Valid Palindrome',
            'slug': 'valid-palindrome',
            'difficulty': 'easy',
            'category': 'Strings',
            'description': 'Given a string `s`, return "true" if it is a palindrome considering only alphanumeric characters and ignoring cases, otherwise return "false".',
            'input_format': 'A single line containing string s.',
            'output_format': 'Print "true" or "false".',
            'constraints': '1 <= s.length <= 2 * 10^5',
            'sample_input': 'A man, a plan, a canal: Panama',
            'sample_output': 'true',
            'starter_code': 'import sys\n\ndef solve():\n    s = sys.stdin.read().strip()\n    filtered = "".join([c.lower() for c in s if c.isalnum()])\n    if filtered == filtered[::-1]:\n        print("true")\n    else:\n        print("false")\n\nif __name__ == "__main__":\n    solve()\n',
            'test_cases': [
                {'input': 'A man, a plan, a canal: Panama', 'expected': 'true', 'is_hidden': False},
                {'input': 'race a car', 'expected': 'false', 'is_hidden': False},
                {'input': 'Was it a car or a cat I saw?', 'expected': 'true', 'is_hidden': True},
                {'input': 'hello', 'expected': 'false', 'is_hidden': True}
            ]
        },
        {
            'title': 'Maximum Subarray (Kadane\'s Algorithm)',
            'slug': 'maximum-subarray',
            'difficulty': 'medium',
            'category': 'Dynamic Programming',
            'description': 'Given an integer array `nums`, find the subarray with the largest sum, and return its sum.',
            'input_format': 'First line contains space-separated integers of array nums.',
            'output_format': 'Print a single integer representing the maximum subarray sum.',
            'constraints': '1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
            'sample_input': '-2 1 -3 4 -1 2 1 -5 4',
            'sample_output': '6',
            'starter_code': 'import sys\n\ndef solve():\n    nums = list(map(int, sys.stdin.read().split()))\n    max_sum = nums[0]\n    current_sum = nums[0]\n    for x in nums[1:]:\n        current_sum = max(x, current_sum + x)\n        max_sum = max(max_sum, current_sum)\n    print(max_sum)\n\nif __name__ == "__main__":\n    solve()\n',
            'test_cases': [
                {'input': '-2 1 -3 4 -1 2 1 -5 4', 'expected': '6', 'is_hidden': False},
                {'input': '1', 'expected': '1', 'is_hidden': False},
                {'input': '5 4 -1 7 8', 'expected': '23', 'is_hidden': True},
                {'input': '-3 -2 -1 -4', 'expected': '-1', 'is_hidden': True}
            ]
        },
        {
            'title': 'Merge Two Sorted Arrays',
            'slug': 'merge-two-sorted-arrays',
            'difficulty': 'medium',
            'category': 'Searching & Sorting',
            'description': 'Given two sorted integer arrays, merge them into a single sorted array.',
            'input_format': 'First line: space-separated integers for array 1.\nSecond line: space-separated integers for array 2.',
            'output_format': 'Print the merged sorted integers separated by space.',
            'constraints': '0 <= len(arr1), len(arr2) <= 10^4',
            'sample_input': '1 3 5 7\n2 4 6 8',
            'sample_output': '1 2 3 4 5 6 7 8',
            'starter_code': 'import sys\n\ndef solve():\n    lines = sys.stdin.read().splitlines()\n    a1 = list(map(int, lines[0].split())) if len(lines) > 0 and lines[0].strip() else []\n    a2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\n    merged = sorted(a1 + a2)\n    print(" ".join(map(str, merged)))\n\nif __name__ == "__main__":\n    solve()\n',
            'test_cases': [
                {'input': '1 3 5 7\n2 4 6 8', 'expected': '1 2 3 4 5 6 7 8', 'is_hidden': False},
                {'input': '1 2 3\n4 5 6', 'expected': '1 2 3 4 5 6', 'is_hidden': False},
                {'input': '10 20\n5 15 25', 'expected': '5 10 15 20 25', 'is_hidden': True}
            ]
        }
    ]

    for cp_data in coding_problems:
        tc = cp_data.pop('test_cases')
        cp = CodingProblem(**cp_data)
        cp.set_test_cases(tc)
        db.session.add(cp)
    db.session.commit()

    # 5. Seed a Sample Test Result for Student
    demo_result = TestResult(
        student_id=student.id,
        test_id=apt_test.id,
        category='aptitude',
        score=40.0,
        total_marks=50.0,
        total_questions=10,
        correct_answers=8,
        incorrect_answers=2,
        unanswered=0,
        percentage=80.0,
        time_taken_seconds=540,
        passed=True,
        answers_json=json.dumps({'1': 'B', '2': 'B', '3': 'A', '4': 'A', '5': 'A'})
    )
    db.session.add(demo_result)

    # 6. Seed Student Progress
    progress_apt = StudentProgress(
        student_id=student.id,
        category='aptitude',
        subcategory='quantitative',
        tests_taken=1,
        questions_attempted=10,
        correct_count=8,
        accuracy_percentage=80.0,
        time_spent_seconds=540,
        mastery_level='Advanced'
    )
    db.session.add(progress_apt)

    # 7. Seed Initial Recommendations
    rec1 = Recommendation(
        student_id=student.id,
        recommendation_type='coding',
        title='Practice Dynamic Programming & Arrays',
        description='Sharpen your problem-solving speed by solving standard Kadane\'s Algorithm and Two Sum questions.',
        reason='Coding challenges carry 35% weight in technical placement drives.',
        suggested_action='Complete Two Sum and Maximum Subarray challenges.',
        action_url='/coding',
        priority='high',
        is_completed=False
    )
    rec2 = Recommendation(
        student_id=student.id,
        recommendation_type='resume',
        title='Upload Resume for AI ATS Scoring',
        description='Upload your resume to check keywords, formatting, and role alignment with current campus recruitments.',
        reason='No resume uploaded yet for ATS evaluation.',
        suggested_action='Upload PDF/DOCX resume.',
        action_url='/resume/upload',
        priority='high',
        is_completed=False
    )
    rec3 = Recommendation(
        student_id=student.id,
        recommendation_type='interview',
        title='Simulate AI Technical Interview',
        description='Practice speaking through OOP, DBMS, and OS questions with immediate AI scoring.',
        reason='Interview readiness is critical for final selection.',
        suggested_action='Complete a 5-question Technical mock interview.',
        action_url='/interview',
        priority='medium',
        is_completed=False
    )
    db.session.add_all([rec1, rec2, rec3])
    db.session.commit()

