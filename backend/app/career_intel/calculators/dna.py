def build_career_dna(scores, skills):
    # Simple DNA: strengths and focus areas
    strengths = sorted(skills.items(), key=lambda x: x[1], reverse=True)[:5]
    dna = {
        'strengths': [s for s, v in strengths],
        'dominant_skill': strengths[0][0] if strengths else None,
        'score_snapshot': {k: v for k, v in scores.items()},
    }
    return dna
