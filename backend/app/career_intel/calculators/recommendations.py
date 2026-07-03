def generate_recommendations(scores, gaps, benchmarks):
    recs = []
    # For large skill gaps produce learning recs
    for g in gaps[:5]:
        impact = round(g['gap_score'] * 10, 2)
        recs.append({
            'id': f'rec_skill_{g["skill"]}',
            'text': f'Learn {g["skill"]} to close a {g["gap_score"]*100:.0f}% gap',
            'impact_estimate': impact,
            'effort_estimate': '4-10 hrs',
            'difficulty': 'Medium' if g['gap_score'] > 0.3 else 'Easy',
            'confidence': 0.6 + min(0.3, g['gap_score']),
            'roi': {'careerScoreDelta': round(impact * 0.5, 2), 'jobMatchDelta': round(impact * 0.7, 2), 'salaryImpact': round(benchmarks.get('salary_median', 90000) * 0.01 * impact, 2)}
        })

    # Generic resume improvement rec
    recs.append({'id': 'rec_resume_metrics', 'text': 'Add measurable achievements to resume', 'impact_estimate': 5, 'effort_estimate': '1-3 hrs', 'difficulty': 'Easy', 'confidence': 0.8, 'roi': {'careerScoreDelta': 2, 'jobMatchDelta': 3}})

    return recs
