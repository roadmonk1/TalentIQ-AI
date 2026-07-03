import logging
from app.career_intel.config import DEFAULT_WEIGHTS, BENCHMARKS
from app.career_intel.calculators.career import calculate_career_score
from app.career_intel.calculators.resume import calculate_resume_score
from app.career_intel.calculators.ats import calculate_ats_score
from app.career_intel.calculators.skillgap import calculate_skill_gaps
from app.career_intel.calculators.match import calculate_job_match
from app.career_intel.calculators.recommendations import generate_recommendations
from app.career_intel.calculators.dna import build_career_dna

logger = logging.getLogger('app.career_intel')


class CareerIntelService:
    @staticmethod
    def calculate_for(context, target_career='default'):
        """
        context: dict containing profile, resume_text, skills, activity, candidate_jobs
        returns structured results with explainable breakdowns, confidence, benchmarks, and ROI estimates.
        """
        weights = DEFAULT_WEIGHTS.get(target_career, DEFAULT_WEIGHTS['default'])
        benchmarks = BENCHMARKS.get(target_career, BENCHMARKS['default'])

        profile = context.get('profile', {})
        resume_text = context.get('resume_text', '')
        skills = context.get('skills', {})
        activity = context.get('activity', {})
        candidate_jobs = context.get('jobs', [])
        target_skills = context.get('target_skills', {})

        # Calculate scores
        career = calculate_career_score(profile, skills, activity, weights['career'])
        resume = calculate_resume_score(resume_text, list(target_skills.keys()), weights['resume'])
        ats = calculate_ats_score(resume_text, list(target_skills.keys()), weights['ats'])

        # Skill gaps
        gaps = calculate_skill_gaps(skills, target_skills)

        # Job matches
        job_matches = []
        for j in candidate_jobs:
            jm = calculate_job_match(skills, j.get('requirements', {}), ats['value'], weights['match'])
            jm['job_id'] = j.get('id')
            job_matches.append(jm)

        # Recommendations
        recs = generate_recommendations({'career': career, 'resume': resume}, gaps, benchmarks)

        # Career DNA
        dna = build_career_dna({'career': career['value'], 'resume': resume['value']}, skills)

        result = {
            'scores': {
                'careerScore': career,
                'resumeScore': resume,
                'atsScore': ats,
            },
            'skillGaps': gaps,
            'jobMatches': job_matches,
            'recommendations': recs,
            'careerDNA': dna,
            'benchmarks': benchmarks,
        }

        logger.debug('Calculated career intel for target=%s', target_career)
        return result
