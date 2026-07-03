def calculate_job_match(candidate_skills, job_requirements, ats_score, weights):
    # compute skill overlap
    matched = 0.0
    total = 0.0
    reasons = []
    missing = []
    for skill, req_level in job_requirements.items():
        total += req_level
        cand = candidate_skills.get(skill, 0.0)
        matched += min(cand, req_level)
        if cand < req_level:
            missing.append(skill)
            reasons.append(f'Missing {skill} (need {req_level}, have {cand})')

    skill_alignment = (matched / total) if total > 0 else 0
    value = (skill_alignment * weights.get('skills', 0) + (min(1.0, ats_score / 100.0) * weights.get('ats', 0)) + weights.get('experience', 0) * 0.8) * 100
    confidence = 0.7
    return {'match_pct': round(value), 'reasons': reasons, 'missing_skills': missing, 'confidence': confidence}
