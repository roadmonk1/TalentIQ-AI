import logging
from .validation import validate_upload
from .parsers.pdf_parser import extract_text_from_pdf_bytes
from .parsers.docx_parser import extract_text_from_docx_bytes
from .normalizer import sectionize_text, extract_contacts, extract_skills, extract_experience, detect_quantified_achievements, compute_resume_completeness, detect_risks
from app.career_intel.service import CareerIntelService
from datetime import datetime

logger = logging.getLogger('app.resume_pipeline.service')


class TalentParseService:
    STAGES = ['Uploading', 'Parsing', 'Extracting', 'Analyzing', 'Calculating', 'Complete']

    @staticmethod
    def process_resume(filename: str, file_bytes: bytes, user_id=None, target_career='default'):
        stages = []
        def mark(stage, note=None):
            stages.append({'stage': stage, 'timestamp': datetime.utcnow().isoformat() + 'Z', 'note': note})

        # Validation
        mark('Uploading')
        valid, reason, meta = validate_upload(filename, file_bytes)
        if not valid:
            mark('Complete', {'status': 'failed', 'reason': reason})
            return {'status': 'failed', 'reason': reason, 'stages': stages}

        # Parsing
        mark('Parsing')
        text = ''
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf_bytes(file_bytes)
        elif filename.lower().endswith('.docx'):
            text = extract_text_from_docx_bytes(file_bytes)

        if not text or len(text.strip()) < 50:
            # could be scanned PDF or extraction failure
            mark('Complete', {'status': 'failed', 'reason': 'extraction_empty_or_scanned'})
            return {'status': 'failed', 'reason': 'extraction_empty_or_scanned', 'stages': stages}

        # Extracting
        mark('Extracting')
        sections = sectionize_text(text)
        contacts = extract_contacts(text)
        skills = extract_skills(sections)
        experiences = extract_experience(sections)
        achievements = detect_quantified_achievements(text)

        # Analyzing
        mark('Analyzing')
        completeness = compute_resume_completeness(sections)
        risks = detect_risks(sections, {})

        # Build normalized profile
        profile = {
            'id': user_id or 'anon',
            'contacts': contacts,
            'sections': sections,
            'skills': skills,
            'experiences': experiences,
            'achievements': achievements,
            'raw_text': text,
            'metadata': {'word_count': len(text.split()), 'file_name': filename},
            'completeness': completeness,
            'risks': risks,
            'version': 1,
        }

        # Resume Health Score: deterministic metric based on completeness and risks
        resume_health = int(min(100, (completeness * 80) + (max(0, 1 - len(risks) * 0.5) * 20)))
        profile['resume_health'] = {'value': resume_health, 'breakdown': [{'label': 'completeness', 'value': completeness * 100}, {'label': 'risks_penalty', 'value': (1 - min(1, len(risks) * 0.5)) * 100}], 'confidence': 0.85}

        # store timeline events
        profile.setdefault('timeline', [])
        profile['timeline'].append({'id': f'upload_{datetime.utcnow().timestamp()}', 'text': 'Resume uploaded', 'when': datetime.utcnow().isoformat() + 'Z'})

        # Calculating: call CareerIntelService
        mark('Calculating')
        # convert skills to vector {skill: proficiency}
        skill_vector = {k: v.get('confidence', 0.5) for k, v in skills.items()}
        context = {'profile': {'profile_completion': completeness}, 'resume_text': text, 'skills': skill_vector, 'jobs': [], 'target_skills': {}}
        intel = CareerIntelService.calculate_for(context, target_career=target_career)

        # final timeline event
        profile['timeline'].append({'id': f'analysis_{datetime.utcnow().timestamp()}', 'text': 'Resume analyzed', 'when': datetime.utcnow().isoformat() + 'Z'})

        mark('Complete')

        # store latest processed profile in-memory for demo purposes
        try:
            _store_latest_profile(profile.get('id') or meta.get('hash'), {'profile': profile, 'intel': intel, 'meta': meta, 'stages': stages})
        except Exception:
            logger.exception('Failed to store latest profile')

        return {
            'status': 'ok',
            'profile': profile,
            'intel': intel,
            'stages': stages,
            'meta': meta,
        }

    @staticmethod
    def process_text_resume(text: str, filename: str = 'demo.txt', user_id=None, target_career='default'):
        """Process a plain text resume for demo/testing without file parsing/validation."""
        stages = []
        def mark(stage, note=None):
            stages.append({'stage': stage, 'timestamp': datetime.utcnow().isoformat() + 'Z', 'note': note})

        mark('Parsing')
        mark('Extracting')
        sections = sectionize_text(text)
        contacts = extract_contacts(text)
        skills = extract_skills(sections)
        experiences = extract_experience(sections)
        achievements = detect_quantified_achievements(text)

        mark('Analyzing')
        completeness = compute_resume_completeness(sections)
        risks = detect_risks(sections, {})

        profile = {
            'id': user_id or 'anon',
            'contacts': contacts,
            'sections': sections,
            'skills': skills,
            'experiences': experiences,
            'achievements': achievements,
            'raw_text': text,
            'metadata': {'word_count': len(text.split()), 'file_name': filename},
            'completeness': completeness,
            'risks': risks,
            'version': 1,
        }

        resume_health = int(min(100, (completeness * 80) + (max(0, 1 - len(risks) * 0.5) * 20)))
        profile['resume_health'] = {'value': resume_health, 'breakdown': [{'label': 'completeness', 'value': completeness * 100}, {'label': 'risks_penalty', 'value': (1 - min(1, len(risks) * 0.5)) * 100}], 'confidence': 0.85}
        profile.setdefault('timeline', [])
        profile['timeline'].append({'id': f'upload_{datetime.utcnow().timestamp()}', 'text': 'Resume uploaded (demo)', 'when': datetime.utcnow().isoformat() + 'Z'})

        mark('Calculating')
        skill_vector = {k: v.get('confidence', 0.5) for k, v in skills.items()}
        context = {'profile': {'profile_completion': completeness}, 'resume_text': text, 'skills': skill_vector, 'jobs': [], 'target_skills': {}}
        intel = CareerIntelService.calculate_for(context, target_career=target_career)

        profile['timeline'].append({'id': f'analysis_{datetime.utcnow().timestamp()}', 'text': 'Resume analyzed (demo)', 'when': datetime.utcnow().isoformat() + 'Z'})

        mark('Complete')

        try:
            _store_latest_profile(profile.get('id') or filename, {'profile': profile, 'intel': intel, 'meta': {'demo': True}, 'stages': stages})
        except Exception:
            logger.exception('Failed to store latest profile')

        return {'status': 'ok', 'profile': profile, 'intel': intel, 'stages': stages}


# In-memory store for latest profiles (demo only fallback)
_latest_profiles = {}


def _store_latest_profile(key, payload):
    if not key:
        key = 'anon'
    try:
        from app.resume_pipeline.resume_repository import ResumeRepository
        profile = payload.get('profile')
        intel = payload.get('intel')
        meta = payload.get('meta')
        stages = payload.get('stages')
        filename = (profile.get('metadata', {}).get('file_name') if profile else None) or 'resume.pdf'
        
        ResumeRepository.save_profile(
            user_id=key,
            filename=filename,
            text=profile.get('raw_text', '') if profile else '',
            parsed_profile=profile,
            intel=intel,
            meta=meta,
            stages=stages
        )
    except Exception as exc:
        logger.error("DB failed to store profile for %s, falling back to in-memory: %s", key, exc)
        
    _latest_profiles[key] = payload


def get_latest_profile(key=None):
    if not key:
        key = 'anon'
    try:
        from app.resume_pipeline.resume_repository import ResumeRepository
        db_profile = ResumeRepository.get_latest_profile(key)
        if db_profile:
            return db_profile
    except Exception as exc:
        logger.error("DB failed to read profile for %s, trying in-memory: %s", key, exc)
        
    return _latest_profiles.get(key)
