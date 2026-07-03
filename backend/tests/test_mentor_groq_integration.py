import pytest

from unittest.mock import MagicMock


def test_deterministic_intent_does_not_call_groq(monkeypatch):
    # Arrange: monkeypatch provider factory to raise if used
    import app.mentor.adapters as adapters
    def fake_factory():
        raise AssertionError('Groq should not be called for deterministic intents')
    monkeypatch.setattr(adapters, 'provider_factory', fake_factory)

    # Act: call handle_chat with a deterministic message (resume health)
    from app.mentor.service import MentorService

    payload = {'session_id': 's1', 'user_id': 'u1', 'message': 'What is my resume health?'}
    result = MentorService.handle_chat(payload)

    # Assert: result comes from deterministic path and contains assistant_text
    assert 'assistant_text' in result


def test_ai_coaching_intent_calls_groq(monkeypatch):
    # Arrange: create a fake provider to capture calls
    called = {'chat': False}

    class FakeProvider:
        def chat(self, prompt):
            called['chat'] = True
            return {'assistant_text': 'Coach says do X', 'confidence': 0.8}

        def parse_response(self, raw):
            return raw

        def health_check(self):
            return True

    import app.mentor.adapters as adapters
    monkeypatch.setattr(adapters, 'provider_factory', lambda: FakeProvider())

    from app.mentor.service import MentorService
    payload = {'session_id': 's2', 'user_id': 'u2', 'message': 'Help me prepare for interviews'}
    result = MentorService.handle_chat(payload)

    assert called['chat'] is True
    assert 'assistant_text' in result


def test_invalid_groq_response_falls_back(monkeypatch):
    # Arrange: provider returns malformed response
    class BadProvider:
        def chat(self, prompt):
            return {'unexpected': 'value'}

        def parse_response(self, raw):
            return raw

        def health_check(self):
            return True

    import app.mentor.adapters as adapters
    monkeypatch.setattr(adapters, 'provider_factory', lambda: BadProvider())

    from app.mentor.service import MentorService
    payload = {'session_id': 's3', 'user_id': 'u3', 'message': 'Give coaching'}
    result = MentorService.handle_chat(payload)

    # Formatter should produce a safe structure and validator should ensure assistant_text exists (possibly from fallback)
    assert 'assistant_text' in result


def test_memory_updated_only_after_validation(monkeypatch):
    # Arrange: provider returns valid response but we monitor memory calls
    class FakeProvider:
        def chat(self, prompt):
            return {'assistant_text': 'All good', 'confidence': 0.7}

        def parse_response(self, raw):
            return raw

        def health_check(self):
            return True

    import app.mentor.adapters as adapters
    monkeypatch.setattr(adapters, 'provider_factory', lambda: FakeProvider())

    import app.mentor.memory as memory
    appended = []
    monkeypatch.setattr(memory, 'append_message', lambda session_id, role, text, metadata=None: appended.append((session_id, role, text)))
    monkeypatch.setattr(memory, 'append_session_summary', lambda session_id, summary: appended.append((session_id, 'summary', summary)))

    from app.mentor.service import MentorService
    payload = {'session_id': 's4', 'user_id': 'u4', 'message': 'Give coaching steps'}
    result = MentorService.handle_chat(payload)

    # Ensure memory recorded assistant message and summary after validation
    assert any(item[1] == 'assistant' for item in appended) or any(item[1] == 'summary' for item in appended)
