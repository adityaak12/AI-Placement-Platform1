-- AI Placement Preparation Platform Seed Data
-- Demo administrator: admin@placement.edu (Password: Admin@123)
-- Demo student: student@placement.edu (Password: Student@123)

INSERT INTO users (name, email, password_hash, role, college, degree, graduation_year, target_role, skills, bio)
VALUES 
('Admin Officer', 'admin@placement.edu', 'scrypt:32768:8:1$7f3zC2K...$hashplaceholder', 'admin', 'Campus Placement Cell', 'Administration', 2024, 'Placement Administrator', 'Administration, Campus Recruitment, Analytics', 'Lead Placement Coordinator.'),
('Aditya Madne', 'student@placement.edu', 'scrypt:32768:8:1$7f3zC2K...$hashplaceholder', 'student', 'Government College of Engineering', 'B.Tech in Computer Science', 2026, 'Software Engineer', 'Python, Java, C++, SQL, React, Git', 'Final year engineering student preparing for campus recruitment.');

INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_option, category, subcategory, difficulty, explanation)
VALUES
('A and B together can complete a work in 12 days, while B alone can finish it in 30 days. In how many days can A alone finish the work?', '18 days', '20 days', '24 days', '15 days', 'B', 'aptitude', 'quantitative', 'medium', '1/A = 1/12 - 1/30 = 3/60 = 1/20. Thus A takes 20 days.'),
('A train 240 m long passes a pole in 24 seconds. How long will it take to pass a platform 650 m long?', '65 seconds', '89 seconds', '100 seconds', '75 seconds', 'B', 'aptitude', 'quantitative', 'medium', 'Speed = 240/24 = 10 m/s. Time = (240+650)/10 = 89 seconds.'),
('Find the next number in the series: 3, 7, 15, 31, 63, ?', '127', '126', '128', '125', 'A', 'aptitude', 'logical', 'easy', 'Pattern: (x * 2) + 1. 63 * 2 + 1 = 127.'),
('What is the worst-case time complexity of QuickSort?', 'O(N log N)', 'O(N)', 'O(N^2)', 'O(log N)', 'C', 'technical', 'dsa', 'medium', 'In worst case (poor pivot), QuickSort degrades to O(N^2).'),
('Which normal form eliminates partial functional dependency on the primary key?', '1NF', '2NF', '3NF', 'BCNF', 'B', 'technical', 'dbms', 'medium', '2NF eliminates partial dependency.');

