"""
Configurable weighting and benchmarks for Career Intelligence Engine.
Weights are defined per target career; product owners can edit this JSON-like config.
"""

DEFAULT_WEIGHTS = {
    'default': {
        'career': {'skills': 0.4, 'experience': 0.2, 'activity': 0.15, 'profile': 0.15, 'visibility': 0.1},
        'resume': {'keywords': 0.45, 'achievements': 0.25, 'structure': 0.15, 'links': 0.1, 'readability': 0.05},
        'ats': {'keywords': 0.6, 'synonyms': 0.15, 'structure': 0.15, 'format': 0.1},
        'match': {'skills': 0.6, 'experience': 0.2, 'ats': 0.1, 'culture': 0.1},
        'interview': {'technical': 0.5, 'behavioral': 0.25, 'practice': 0.15, 'domain': 0.1},
    }
}

# Industry benchmarks (example values) used for comparison
BENCHMARKS = {
    'frontend': {'career_median': 68, 'resume_median': 74, 'ats_median': 80, 'salary_median': 95000},
    'backend': {'career_median': 66, 'resume_median': 72, 'ats_median': 78, 'salary_median': 100000},
    'default': {'career_median': 60, 'resume_median': 65, 'ats_median': 70, 'salary_median': 90000},
}
