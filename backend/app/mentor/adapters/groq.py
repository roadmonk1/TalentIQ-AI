import os
import requests
from app.mentor.adapters.base import BaseAIProvider


class GroqProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.endpoint = os.getenv('GROQ_API_URL', 'https://api.groq.com/v1')

        if not self.api_key:
            # Delay raising to allow health_check to surface a friendly error
            self._missing_key = True
        else:
            self._missing_key = False
        # optional model name from env
        self.model_name = os.getenv('GROQ_MODEL', 'groq-default')

    def chat(self, prompt):
        if getattr(self, '_missing_key', False):
            raise EnvironmentError('GROQ_API_KEY is not set in environment')
        # Send only structured prompt parts to Groq
        payload = {
            'system_prompt': prompt.system_prompt,
            'context': prompt.context,
            'user_prompt': prompt.user_prompt,
            'version': prompt.version,
        }
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        try:
            response = requests.post(f'{self.endpoint}/chat', json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            # Surface a controlled error for the orchestration layer
                raise RuntimeError(f'Groq provider request failed: {str(exc)}')

    def health_check(self):
        # Minimal check: ensure API key present and try a lightweight ping if possible
        if getattr(self, '_missing_key', False):
            raise EnvironmentError('GROQ_API_KEY missing')
        try:
            # perform a lightweight request to the endpoint root or ping path
            r = requests.get(self.endpoint, headers={'Authorization': f'Bearer {self.api_key}'}, timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def parse_response(self, raw_response):
        # Try to extract the common structured fields if present, otherwise return raw
        if not raw_response:
            return {}

        # Common Groq shapes may include top-level fields or nested under 'data'/'result'
        if isinstance(raw_response, dict):
            # unwrap common keys
            candidate = raw_response.get('data') or raw_response.get('result') or raw_response.get('response') or raw_response
            # if candidate is dict and has assistant_text, return it
            if isinstance(candidate, dict) and 'assistant_text' in candidate:
                return candidate
            # otherwise, attempt to find textual assistant output
            text = None
            for key in ('assistant_text', 'text', 'reply', 'output'):
                if key in candidate:
                    text = candidate.get(key)
                    break
            if text:
                return {'assistant_text': text}

        # Fallback: return the raw response so the formatter can normalize it
        return {'raw': raw_response}
