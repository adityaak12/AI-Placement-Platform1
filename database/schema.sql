-- AI Placement Preparation Platform Database Schema
-- Compatible with MySQL and SQLite

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    college VARCHAR(150),
    degree VARCHAR(100),
    graduation_year INT,
    target_role VARCHAR(100) DEFAULT 'Software Engineer',
    skills TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    option_a VARCHAR(500) NOT NULL,
    option_b VARCHAR(500) NOT NULL,
    option_c VARCHAR(500) NOT NULL,
    option_d VARCHAR(500) NOT NULL,
    correct_option VARCHAR(5) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(80) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'medium',
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(80),
    duration_minutes INT DEFAULT 30,
    total_marks INT DEFAULT 100,
    passing_marks INT DEFAULT 40,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INT NOT NULL,
    question_id INT NOT NULL,
    order_num INT DEFAULT 0,
    marks INT DEFAULT 1,
    FOREIGN KEY(test_id) REFERENCES tests(id) ON DELETE CASCADE,
    FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS coding_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    difficulty VARCHAR(20) DEFAULT 'medium',
    category VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    input_format TEXT,
    output_format TEXT,
    constraints TEXT,
    sample_input TEXT,
    sample_output TEXT,
    test_cases_json TEXT,
    starter_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coding_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    problem_id INT NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(30) DEFAULT 'python',
    status VARCHAR(40) DEFAULT 'Pending',
    passed_tests INT DEFAULT 0,
    total_tests INT DEFAULT 0,
    score REAL DEFAULT 0.0,
    execution_time_ms REAL DEFAULT 0.0,
    error_message TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(problem_id) REFERENCES coding_problems(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interview_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    interview_type VARCHAR(30) NOT NULL,
    target_role VARCHAR(100) DEFAULT 'Software Engineer',
    status VARCHAR(20) DEFAULT 'in_progress',
    messages_json TEXT,
    current_question_index INT DEFAULT 0,
    overall_score REAL DEFAULT 0.0,
    technical_score REAL DEFAULT 0.0,
    communication_score REAL DEFAULT 0.0,
    confidence_score REAL DEFAULT 0.0,
    feedback_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resume_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    target_role VARCHAR(100) DEFAULT 'Software Engineer',
    ats_score REAL DEFAULT 0.0,
    matched_skills_json TEXT,
    missing_skills_json TEXT,
    sections_detected_json TEXT,
    feedback_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    test_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    score REAL DEFAULT 0.0,
    total_marks REAL DEFAULT 100.0,
    total_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    incorrect_answers INT DEFAULT 0,
    unanswered INT DEFAULT 0,
    percentage REAL DEFAULT 0.0,
    time_taken_seconds INT DEFAULT 0,
    passed BOOLEAN DEFAULT 0,
    answers_json TEXT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(test_id) REFERENCES tests(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(80),
    tests_taken INT DEFAULT 0,
    questions_attempted INT DEFAULT 0,
    correct_count INT DEFAULT 0,
    accuracy_percentage REAL DEFAULT 0.0,
    time_spent_seconds INT DEFAULT 0,
    mastery_level VARCHAR(30) DEFAULT 'Beginner',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT NOT NULL,
    recommendation_type VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    reason VARCHAR(255),
    suggested_action VARCHAR(255),
    action_url VARCHAR(255),
    priority VARCHAR(20) DEFAULT 'medium',
    is_completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
);

