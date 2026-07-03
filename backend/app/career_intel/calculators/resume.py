def calculate_resume_score(resume_text, keywords, weights):
    # naive keyword match count
    text = (resume_text or '').lower()
    matched = 0
    for k in keywords:
        if k.lower() in text:
            matched += 1
    keyword_score = (matched / max(len(keywords), 1))

    # simple readability proxy: length in words
    words = len(text.split())
    length_score = 1.0 if 300 <= words <= 800 else max(0.5, min(1.0, words / 800))

    achievements = 0.5 if 'achieved' in text or 'increased' in text or '%' in text else 0.2

    parts = {
        'Keywords': round(keyword_score * 100 * weights.get('keywords', 0), 2),
        'Achievements': round(achievements * 100 * weights.get('achievements', 0), 2),
        'Structure': round(length_score * 100 * weights.get('structure', 0), 2),
        'Links': round((1.0 if 'http' in text else 0.0) * 100 * weights.get('links', 0), 2),
        'Readability': round(length_score * 100 * weights.get('readability', 0), 2),
    }

    value = sum(parts.values())
    breakdown = [{'label': k, 'value': v} for k, v in parts.items()]
    confidence = 0.75
    return {'value': round(value), 'breakdown': breakdown, 'confidence': confidence}
