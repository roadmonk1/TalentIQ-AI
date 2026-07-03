from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/')
def health():
    return jsonify({'status': 'ok', 'service': 'talentiq-ai-backend'})


@app.get('/api/health')
def api_health():
    return jsonify({'status': 'ok', 'message': 'Backend ready'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
