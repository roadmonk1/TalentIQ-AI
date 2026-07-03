def calculate_ats_score(resume_text, keywords, weights):
    text = (resume_text or '').lower()
    matched = 0
    for k in keywords:
        if k.lower() in text:
            matched += 1
    keyword_exact = (matched / max(len(keywords), 1))

    # penalize tables/columns by naive check
    has_tables = ('<table>' in resume_text or '\t' in resume_text) if resume_text else False
    format_penalty = 0.8 if has_tables else 1.0

    parts = {
        'KeywordExact': round(keyword_exact * 100 * weights.get('keywords', 0), 2),
        'Synonyms': round(min(0.2 + keyword_exact * 0.8, 1.0) * 100 * weights.get('synonyms', 0), 2),
        'Structure': round(100 * weights.get('structure', 0) * (0.9 if has_tables else 1.0), 2),
        'Format': round(100 * weights.get('format', 0) * format_penalty, 2),
    }

    value = sum(parts.values())
    confidence = 0.7
    breakdown = [{'label': k, 'value': v} for k, v in parts.items()]
    return {'value': round(value), 'breakdown': breakdown, 'confidence': confidence}
