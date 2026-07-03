import os
from app.mentor.adapters.groq import GroqProvider


def provider_factory():
    provider_name = os.getenv('AI_PROVIDER', 'groq').lower()
    if provider_name == 'groq':
        return GroqProvider()
    raise ValueError(f'Unsupported AI provider: {provider_name}')
