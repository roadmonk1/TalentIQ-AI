def calculate_career_score(profile, skills, activity, weights):
    # skills: dict of {skill: proficiency 0-1}
    # profile: contains years_experience and profile_completion 0-1
    skill_avg = 0.0
    if skills:
        skill_avg = sum(skills.values()) / len(skills)

    experience = min(profile.get('years_experience', 0) / 10.0, 1.0)
    activity_score = min(profile.get('recent_activity_count', 0) / 10.0, 1.0)
    profile_completion = profile.get('profile_completion', 0)

    parts = {
        'Skills': round(skill_avg * 100 * weights.get('skills', 0), 2),
        'Experience': round(experience * 100 * weights.get('experience', 0), 2),
        'Activity': round(activity_score * 100 * weights.get('activity', 0), 2),
        'Profile': round(profile_completion * 100 * weights.get('profile', 0), 2),
        'Visibility': round((1.0 if profile.get('is_verified') else 0.4) * 100 * weights.get('visibility', 0), 2),
    }

    value = sum(parts.values())
    breakdown = [{'label': k, 'value': v} for k, v in parts.items()]
    confidence = 0.8 if skills else 0.5
    return {'value': round(value), 'breakdown': breakdown, 'confidence': confidence}
