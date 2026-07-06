import logging
import uuid
from datetime import datetime
from app.career_intel.service import CareerIntelService
from app.resume_pipeline.service import get_latest_profile

logger = logging.getLogger('app.dashboard')


def is_uuid(val):
    if not val:
        return False
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


class DashboardService:
    @staticmethod
    def get_dashboard(user_id=None, target_career='default'):
        # If a recently parsed resume exists for this user, use it to populate the dashboard
        stored = get_latest_profile(user_id)
        now = datetime.utcnow().isoformat() + 'Z'
        if stored:
            profile = stored['profile']
            # Fetch user full name from user record if available
            from app.auth.models import User
            try:
                user_record = User.query.filter_by(id=uuid.UUID(user_id)).first() if is_uuid(user_id) else None
                if user_record:
                    profile['full_name'] = user_record.full_name
            except Exception:
                pass
            intel = stored['intel']
            candidate_jobs = []
            payload = {
                'user': profile,
                'scores': {
                    'careerScore': intel['scores']['careerScore']['value'],
                    'resumeScore': intel['scores']['resumeScore']['value'],
                    'breakdowns': {
                        'career': intel['scores']['careerScore']['breakdown'],
                        'resume': intel['scores']['resumeScore']['breakdown'],
                    },
                },
                'missions': {'today': 'No mission for today — check AI Mentor.', 'weeklyGoals': []},
                'ai': {
                    'insights': [{'id': r['id'], 'text': r['text'], 'impact': r.get('impact_estimate', 0), 'confidence': r.get('confidence', 0.6), 'effort': r.get('effort_estimate', '')} for r in intel['recommendations']],
                    'recommendations': [r['text'] for r in intel['recommendations']],
                },
                'jobs': [{'id': jm['job_id'], 'title': '', 'company': '', 'score': jm['match_pct'], 'why': '; '.join(jm.get('reasons', [])), 'missing_skills': jm.get('missing_skills', [])} for jm in intel['jobMatches']],
                'skillGaps': intel['skillGaps'],
                'activity': [],
                'interviews': [],
                'timeline': profile.get('timeline', [{'id': 't1', 'text': 'Career intelligence computed', 'when': now}]),
                'careerDNA': intel.get('careerDNA'),
                'benchmarks': intel.get('benchmarks'),
            }
        elif user_id and is_uuid(user_id):
            # Registered user with no uploaded resume: Empty state!
            payload = {
                'empty_state': True,
                'user': {'full_name': 'New User', 'profile_completion': 0.0},
                'scores': {
                    'careerScore': 0,
                    'resumeScore': 0,
                    'breakdowns': {
                        'career': [],
                        'resume': [],
                    },
                },
                'missions': {'today': 'Upload your resume to get started!', 'weeklyGoals': []},
                'ai': {
                    'insights': [],
                    'recommendations': [],
                },
                'jobs': [],
                'skillGaps': [],
                'activity': [],
                'interviews': [],
                'timeline': [],
                'careerDNA': {},
                'benchmarks': {},
            }
        else:
            # Fallback to demo context
            profile = {'id': user_id or 'demo', 'full_name': 'Demo User', 'profile_completion': 0.78, 'years_experience': 3, 'recent_activity_count': 2, 'is_verified': False}
            # example skills (proficiency 0-1)
            skills = {'React': 0.8, 'JavaScript': 0.9, 'TypeScript': 0.3, 'Docker': 0.2}
            target_skills = {'React': 1.0, 'TypeScript': 0.8, 'AWS': 0.7}
            resume_text = "Demo resume with React and JavaScript experience."
            candidate_jobs = [
                {'id': 'j1', 'title': 'Frontend Engineer', 'company': 'Acme', 'requirements': {'React': 1.0, 'TypeScript': 0.8, 'CSS': 0.6}},
                {'id': 'j2', 'title': 'Fullstack Developer', 'company': 'Beta Co', 'requirements': {'Node.js': 0.8, 'AWS': 0.7}},
            ]

            context = {'profile': profile, 'skills': skills, 'resume_text': resume_text, 'jobs': candidate_jobs, 'target_skills': target_skills, 'activity': {}}

            intel = CareerIntelService.calculate_for(context, target_career=target_career)

            payload = {
                'user': profile,
                'scores': {
                    'careerScore': intel['scores']['careerScore']['value'],
                    'resumeScore': intel['scores']['resumeScore']['value'],
                    'breakdowns': {
                        'career': intel['scores']['careerScore']['breakdown'],
                        'resume': intel['scores']['resumeScore']['breakdown'],
                    },
                },
                'missions': {'today': 'No mission for today — check AI Mentor.', 'weeklyGoals': []},
                'ai': {
                    'insights': [{'id': r['id'], 'text': r['text'], 'impact': r.get('impact_estimate', 0), 'confidence': r.get('confidence', 0.6), 'effort': r.get('effort_estimate', '')} for r in intel['recommendations']],
                    'recommendations': [r['text'] for r in intel['recommendations']],
                },
                'jobs': [{'id': jm['job_id'], 'title': next((j['title'] for j in candidate_jobs if j['id'] == jm['job_id']), ''), 'company': '', 'score': jm['match_pct'], 'why': '; '.join(jm.get('reasons', [])), 'missing_skills': jm.get('missing_skills', [])} for jm in intel['jobMatches']],
                'skillGaps': intel['skillGaps'],
                'activity': [{'id': 'a1', 'text': 'Applied to Frontend Engineer', 'when': now}],
                'interviews': [],
                'timeline': [{'id': 't1', 'text': 'Career intelligence computed', 'when': now}],
                'careerDNA': intel.get('careerDNA'),
                'benchmarks': intel.get('benchmarks'),
            }

        logger.debug('Returning calculated dashboard payload for user_id=%s', user_id)
        return payload

