import re
from dateutil import parser as dateparser
from .config import SKILL_DICTIONARY
import logging

logger = logging.getLogger('app.resume_pipeline.normalizer')


EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE_RE = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}')
URL_RE = re.compile(r'https?://[^\s,]+')


def sectionize_text(text: str):
    # Very basic section detection: split by common headings
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    sections = {'header': [], 'skills': [], 'experience': [], 'education': [], 'projects': [], 'certifications': [], 'other': []}
    current = 'header'
    for line in lines:
        up = line.lower()
        if any(h in up for h in ['skill', 'technical skills', 'skills:']):
            current = 'skills'
            continue
        if any(h in up for h in ['experience', 'work experience', 'professional experience']):
            current = 'experience'
            continue
        if any(h in up for h in ['education', 'academic']):
            current = 'education'
            continue
        if any(h in up for h in ['project', 'projects']):
            current = 'projects'
            continue
        if any(h in up for h in ['certification', 'certifications']):
            current = 'certifications'
            continue

        sections.setdefault(current, []).append(line)

    return sections


def extract_contacts(text: str):
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    urls = URL_RE.findall(text)
    return {'emails': list(dict.fromkeys(emails)), 'phones': list(dict.fromkeys(phones)), 'urls': list(dict.fromkeys(urls))}


def extract_skills(sections):
    skills_text = '\n'.join(sections.get('skills', []) + sections.get('header', []))
    found = {}
    lower = skills_text.lower()
    for canonical, variants in SKILL_DICTIONARY.items():
        for v in variants:
            if v in lower:
                found[canonical] = {'normalized': canonical, 'confidence': 0.9, 'evidence': [{'text': v, 'where': 'skills_section'}]}
                break
    return found


def extract_experience(sections):
    exp_items = []
    for line in sections.get('experience', []):
        # naive parse: look for dates in line
        dates = []
        try:
            parts = line.split('•') if '•' in line else [line]
            for p in parts:
                try:
                    d = dateparser.parse(p, fuzzy=True)
                    dates.append(d.isoformat())
                except Exception:
                    pass
        except Exception:
            pass
        exp_items.append({'text': line, 'dates': dates, 'confidence': 0.6})
    return exp_items


def detect_quantified_achievements(text: str):
    # find patterns like 'increased X by 20%' or 'reduced cost by $10,000'
    patterns = [r'increased[^.\n]{0,80}?\b\d+%?', r'reduced[^.\n]{0,80}?\b\$?\d+[\d,]*', r'achieved[^.\n]{0,80}?\b\d+%?']
    matches = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            matches.append({'text': m.group(0), 'start': m.start(), 'confidence': 0.9})
    return matches


def compute_resume_completeness(sections):
    keys = ['skills', 'experience', 'education', 'projects', 'certifications']
    present = sum(1 for k in keys if sections.get(k))
    completeness = present / len(keys)
    return round(completeness, 2)


def detect_risks(sections, profile):
    risks = []
    # employment gaps: look at experience dates approximate
    # naive: if no experience -> risk
    if not sections.get('experience'):
        risks.append({'type': 'missing_experience', 'message': 'No experience section detected', 'confidence': 0.9})

    # ATS risk: if skills section empty
    if not sections.get('skills'):
        risks.append({'type': 'ats_risk', 'message': 'No skills section; ATS may not parse key skills', 'confidence': 0.8})

    return risks
