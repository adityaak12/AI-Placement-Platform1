# AI Placement Preparation Platform

A comprehensive web-based platform that helps students prepare for campus placements using AI-powered tools — including aptitude and technical practice tests, coding challenges with automated evaluation, AI mock interviews, resume ATS analysis, and personalized learning recommendations.

Academic Year: **2025–2026**

---

## 👥 Team & Module Distribution

| Member | Primary Role | Implemented Modules |
| :--- | :--- | :--- |
| **Member 1: Aditya Madne** | Authentication & Student Portal | Registration, Secure Login, Student Profile, Student Dashboard |
| **Member 2: Om Badhe** | AI Resume Analyzer | Document Text Extraction (PDF/DOCX/TXT), Skill Gap Analysis, ATS Scoring |
| **Member 3: Radha Ghogare** | AI Mock Interview | Technical & HR Rounds, Speech-to-Text Input, Real-time AI Scoring & Feedback |
| **Member 4: Shubham Dighe** | Coding & Assessments | Quantitative, Logical & Verbal Aptitude, In-Platform Python Code Runner & Test Cases |
| **Member 5: Aditya Kshirsagar** | Performance & Recommendations | Multi-domain Performance Analytics, Competency Radar, ML-based Action Recommendations |

---

## ✨ Features & Modules

### 1. 🎯 Practice & Assessments
- **Aptitude Tests:** Quantitative Aptitude, Logical Reasoning, and Verbal Ability practice sets and timed tests.
- **Technical Tests:** Core Computer Science quizzes covering Data Structures & Algorithms, DBMS, Operating Systems, and Computer Networks.
- **Placement Mock Tests:** Timed, full-length placement simulations (mirroring TCS, Infosys, and standard recruitment patterns) with auto-submission and question palettes.

### 2. 💻 Coding Arena
- In-browser code editor with Python 3 execution.
- Sample and hidden test case evaluation with runtime execution metrics.
- Submissions history and problem-solving badges.

### 3. 🤖 AI-Powered Modules
- **AI Resume Analyzer:** Extracts text from PDF, Word (.docx), and plain text; matches against job-role benchmarks; checks essential sections; calculates an ATS score; and generates targeted improvement suggestions.
- **AI Mock Interview Simulator:** Interactive multi-turn interview sessions for Technical and HR rounds with Web Speech API audio input, scoring on technical depth, clarity, and model ideal answers.
- **AI Performance & Recommendation Engine:** Computes subject-wise accuracy, calculates a Placement Readiness Score, identifies strengths and weak areas, and generates prioritized next steps.

### 4. 🛡️ Admin Management Panel
- View all registered student profiles.
- Manage question bank (add/delete aptitude and technical MCQs).
- Create and toggle timed tests.
- View system-wide test results and performance logs.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask 3.x, Flask-Login, Flask-SQLAlchemy, Werkzeug
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js
- **Database:** SQLite (default zero-configuration) / MySQL support
- **Testing:** Pytest

---

## 🚀 Quick Start Guide

### 1. Clone & Navigate
```bash
git clone https://github.com/<your-username>/AI-PLACEMENT-PREPRATION-PLADFORM.git
cd AI-PLACEMENT-PREPRATION-PLADFORM
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```
*The database (`placement.db`) and seed data are automatically initialized on startup.*

Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🔑 Default Demo Credentials

| Role | Email Address | Password |
| :--- | :--- | :--- |
| **Demo Student** | `student@placement.edu` | `Student@123` |
| **Placement Admin** | `admin@placement.edu` | `Admin@123` |

---

## 🧪 Running Unit Tests

Run test suites using `pytest`:
```bash
pytest
```
