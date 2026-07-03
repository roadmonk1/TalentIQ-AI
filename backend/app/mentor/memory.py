import logging
from datetime import datetime

logger = logging.getLogger('app.mentor.memory')

# In-memory stores for alpha/demo
_sessions = {}
_messages = {}
_feedback = {}


class MemoryStore:
    @staticmethod
    def append_message(session_id, role, text, metadata=None):
        _messages.setdefault(session_id, []).append({
            'role': role,
            'text': text,
            'metadata': metadata or {},
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        })

    @staticmethod
    def append_session_summary(session_id, summary):
        session = _sessions.setdefault(session_id, {})
        session['summary'] = summary
        session['updated_at'] = datetime.utcnow().isoformat() + 'Z'

    @staticmethod
    def get_session(session_id):
        return {
            'session_id': session_id,
            'messages': _messages.get(session_id, []),
            'summary': _sessions.get(session_id, {}).get('summary', {}),
        }

    @staticmethod
    def append_feedback(session_id, user_id, message, rating):
        _feedback.setdefault(session_id, []).append({
            'user_id': user_id,
            'message': message,
            'rating': rating,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        })

    @staticmethod
    def summarize_conversation(session_id):
        messages = _messages.get(session_id, [])[-20:]
        return ' '.join([m['text'] for m in messages])


# Module-level compatibility wrappers for tests and external callers
def append_message(session_id, role, text, metadata=None):
    return MemoryStore.append_message(session_id, role, text, metadata=metadata)


def append_session_summary(session_id, summary):
    return MemoryStore.append_session_summary(session_id, summary)


def get_session(session_id):
    return MemoryStore.get_session(session_id)


def append_feedback(session_id, user_id, message, rating):
    return MemoryStore.append_feedback(session_id, user_id, message, rating)


def summarize_conversation(session_id):
    return MemoryStore.summarize_conversation(session_id)
