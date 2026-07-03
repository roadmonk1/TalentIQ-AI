import logging
from flask import Blueprint, request, jsonify
from app.resume_pipeline.service import TalentParseService
from app import limiter

logger = logging.getLogger('app.resume_pipeline.routes')

resume_bp = Blueprint('resume_pipeline', __name__)


@resume_bp.route('/upload', methods=['POST'])
@limiter.limit('10 per minute')
def upload_resume():
    # multipart form: file, user_id, target_career
    f = request.files.get('file')
    user_id = request.form.get('user_id')
    target = request.form.get('target_career', 'default')
    if not f:
        return jsonify({'error': 'no_file'}), 400

    filename = f.filename
    file_bytes = f.read()
    result = TalentParseService.process_resume(filename, file_bytes, user_id=user_id, target_career=target)
    if result.get('status') != 'ok':
        return jsonify({'status': 'failed', 'reason': result.get('reason'), 'stages': result.get('stages')}), 400

    return jsonify({'status': 'ok', 'profile': result['profile'], 'intel': result['intel'], 'stages': result['stages'], 'meta': result.get('meta')}), 200


@resume_bp.route('/demo', methods=['GET'])
def demo_resume():
    # demo text resume to validate end-to-end flow
    demo_text = """
John Doe
Email: john.doe@example.com
Phone: +1 555-123-4567

Summary
Experienced frontend engineer with 5 years building React applications. Increased user engagement by 25%.

Skills
React, JavaScript, TypeScript, CSS, HTML, Docker

Experience
Senior Frontend Engineer — Acme Corp (2019 - Present)
- Built core UI components and improved performance by 30%.

Education
BSc Computer Science — University X (2015 - 2019)

Certifications
Certified Cloud Practitioner — AWS
"""
    result = TalentParseService.process_text_resume(demo_text, filename='demo.txt', user_id='demo_user', target_career='frontend')
    return jsonify(result), 200
