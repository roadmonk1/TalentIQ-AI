def calculate_skill_gaps(candidate_skills, target_skills):
    # candidate_skills, target_skills are dicts {skill: importance/proficiency}
    gaps = []
    for skill, target_level in target_skills.items():
        cand_level = candidate_skills.get(skill, 0.0)
        gap = max(0.0, target_level - cand_level)
        gaps.append({'skill': skill, 'gap_score': round(gap, 3), 'candidate_level': cand_level, 'target_level': target_level})
    # sort by gap_score desc
    gaps.sort(key=lambda x: x['gap_score'], reverse=True)
    return gaps
