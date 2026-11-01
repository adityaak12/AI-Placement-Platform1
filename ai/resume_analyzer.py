import os
import re
import json
import zipfile
import xml.etree.ElementTree as ET


# Role-based skill benchmark requirements
ROLE_SKILL_PROFILES = {
    'Software Engineer': {
        'core': ['python', 'java', 'c++', 'data structures', 'algorithms', 'git', 'sql', 'oops'],
        'preferred': ['docker', 'linux', 'rest api', 'system design', 'ci/cd', 'unit testing'],
    },
    'Full Stack Developer': {
        'core': ['html', 'css', 'javascript', 'react', 'node.js', 'python', 'sql', 'git'],
        'preferred': ['mongodb', 'express', 'typescript', 'docker', 'rest api', 'redux', 'tailwind'],
    },
    'Frontend Developer': {
        'core': ['html', 'css', 'javascript', 'react', 'tailwind', 'bootstrap', 'responsive design'],
        'preferred': ['typescript', 'vue', 'next.js', 'redux', 'figma', 'webpack'],
    },
    'Backend Developer': {
        'core': ['python', 'java', 'sql', 'node.js', 'rest api', 'oops', 'database management', 'git'],
        'preferred': ['django', 'flask', 'spring boot', 'docker', 'redis', 'postgresql', 'microservices'],
    },
    'Data Analyst': {
        'core': ['python', 'sql', 'excel', 'pandas', 'numpy', 'data visualization', 'power bi'],
        'preferred': ['tableau', 'statistics', 'matplotlib', 'seaborn', 'scikit-learn', 'r'],
    },
    'Cloud / DevOps Engineer': {
        'core': ['linux', 'docker', 'kubernetes', 'aws', 'git', 'ci/cd', 'bash'],
        'preferred': ['terraform', 'ansible', 'jenkins', 'azure', 'gcp', 'monitoring', 'python'],
    }
}

ALL_KNOWN_SKILLS = [
    # Languages
    'python', 'java', 'c', 'c++', 'c#', 'javascript', 'typescript', 'php', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'r', 'sql', 'bash',
    # Web & Frameworks
    'html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'spring boot', 'node.js', 'express', 'fastapi', 'next.js', 'tailwind', 'bootstrap',
    # Databases
    'mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'oracle', 'cassandra', 'dynamodb',
    # Cloud & Tools
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github', 'gitlab', 'ci/cd', 'jenkins', 'terraform', 'linux', 'jira',
    # Concepts
    'data structures', 'algorithms', 'oops', 'dbms', 'operating systems', 'computer networks', 'system design', 'rest api', 'graphql',
    # AI/ML & Data
    'machine learning', 'deep learning', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'power bi', 'tableau', 'nlp',
    # Soft skills
    'problem solving', 'teamwork', 'communication', 'leadership', 'adaptability', 'critical thinking'
]


def extract_text_from_file(file_path):
    """Extracts text from PDF, DOCX, or TXT file."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            text = f"Error reading text file: {str(e)}"

    elif ext == '.docx':
        try:
            # Native extraction from DOCX zip XML without external deps
            with zipfile.ZipFile(file_path) as z:
                xml_content = z.read('word/document.xml')
                tree = ET.fromstring(xml_content)
                paragraphs = []
                for node in tree.iter():
                    if node.tag.endswith('}p'):
                        p_text = "".join(node.itertext())
                        if p_text:
                            paragraphs.append(p_text)
                text = "\n".join(paragraphs)
        except Exception:
            try:
                import docx
                doc = docx.Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                text = f"Error reading docx: {str(e)}"

    elif ext == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            pages_text = [page.extract_text() or '' for page in reader.pages]
            text = "\n".join(pages_text)
        except Exception:
            try:
                # Basic stream fallback
                with open(file_path, 'rb') as f:
                    content = f.read().decode('latin-1', errors='ignore')
                    # Find printable blocks
                    found = re.findall(r'\(([^\(\)]+)\)\s*T[jJ]', content)
                    if found:
                        text = " ".join(found)
                    else:
                        text = content[:4000]
            except Exception as e:
                text = f"Error reading pdf: {str(e)}"

    return text


def analyze_resume_content(resume_text, target_role='Software Engineer'):
    """
    Analyzes resume text against target role profile.
    Calculates ATS score, detects sections, extracts skills, identifies gaps,
    and returns rich recommendations.
    """
    clean_text = resume_text.lower()
    role_bench = ROLE_SKILL_PROFILES.get(target_role, ROLE_SKILL_PROFILES['Software Engineer'])

    # 1. Detect Skills
    detected_skills = []
    for skill in ALL_KNOWN_SKILLS:
        # Match as word boundary or exact phrase
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, clean_text):
            detected_skills.append(skill)

    detected_skills = sorted(list(set(detected_skills)))

    # Compare with role expectations
    role_core = role_bench['core']
    role_preferred = role_bench['preferred']

    matched_core = [s for s in role_core if s in detected_skills]
    matched_preferred = [s for s in role_preferred if s in detected_skills]
    missing_core = [s for s in role_core if s not in detected_skills]
    missing_preferred = [s for s in role_preferred if s not in detected_skills]

    # 2. Check Standard Resume Sections
    sections = {
        'contact_info': bool(re.search(r'(@|email|phone|github|linkedin)', clean_text)),
        'education': bool(re.search(r'(education|degree|b\.?tech|b\.?e|university|college|cgpa|gpa)', clean_text)),
        'experience_or_projects': bool(re.search(r'(project|experience|internship|work history)', clean_text)),
        'skills': bool(re.search(r'(skills|technical skills|technologies|tools)', clean_text)),
        'certifications': bool(re.search(r'(certification|certificate|courses|achievements)', clean_text))
    }

    # 3. Calculate ATS Score (0 - 100)
    # Core Skills Match: 35 points
    core_score = (len(matched_core) / max(len(role_core), 1)) * 35

    # Preferred Skills Match: 15 points
    pref_score = (len(matched_preferred) / max(len(role_preferred), 1)) * 15

    # Sections Detected: 25 points (5 pts each)
    section_score = sum(5 for present in sections.values() if present)

    # Content Length & Structure: 15 points
    word_count = len(resume_text.split())
    if 250 <= word_count <= 900:
        length_score = 15
    elif 150 <= word_count < 250 or 900 < word_count <= 1500:
        length_score = 10
    else:
        length_score = 5

    # Action Verbs & Metrics: 10 points
    action_verbs = ['developed', 'implemented', 'designed', 'built', 'created', 'optimized', 'managed', 'led', 'achieved', 'improved']
    found_verbs = [v for v in action_verbs if v in clean_text]
    verb_score = min(len(found_verbs) * 2, 10)

    total_score = min(round(core_score + pref_score + section_score + length_score + verb_score, 1), 100)

    # 4. Generate Targeted Feedback & Actionable Recommendations
    strengths = []
    improvements = []

    if len(matched_core) >= len(role_core) * 0.7:
        strengths.append(f"Strong foundation in core skills for {target_role}: {', '.join(matched_core[:4])}.")
    else:
        improvements.append(f"Add critical missing core skills for {target_role}: {', '.join(missing_core[:3])}.")

    if sections['experience_or_projects']:
        strengths.append("Contains a dedicated Projects or Experience section.")
    else:
        improvements.append("Add a clear 'Projects' or 'Work Experience' section with measurable results.")

    if not sections['certifications']:
        improvements.append("Include relevant technical certifications or hackathon achievements to stand out.")

    if len(found_verbs) < 3:
        improvements.append("Use strong action verbs (e.g., 'Implemented', 'Optimized', 'Engineered') to start bullet points.")

    if word_count < 200:
        improvements.append("Resume content is too brief. Expand on technical project architectures, tools used, and results.")
    elif word_count > 1000:
        improvements.append("Resume is lengthy for campus placement. Aim for a crisp 1-page layout.")

    feedback = {
        'summary': f"Resume evaluated for '{target_role}'. Matched {len(matched_core)} of {len(role_core)} core benchmarks with an overall ATS readiness score of {total_score}%.",
        'word_count': word_count,
        'strengths': strengths,
        'improvements': improvements,
        'action_verbs_found': found_verbs,
        'matched_core_count': len(matched_core),
        'total_core_required': len(role_core),
    }

    return {
        'ats_score': total_score,
        'matched_skills': detected_skills,
        'missing_skills': missing_core + missing_preferred,
        'sections_detected': sections,
        'feedback': feedback
    }

