import logging
from datetime import datetime
from app.mentor.mentor_repository import MentorRepository

logger = logging.getLogger('app.mentor.memory')

# In-memory stores for fallback if database operations fail
_sessions = {}
_messages = {}
_feedback = {}
_memories = {}


class MemoryStore:
    @staticmethod
    def append_message(session_id, role, text, metadata=None):
        """Append message to database, fallback to in-memory store on failure."""
        try:
            MentorRepository.append_message(session_id=session_id, role=role, text=text, metadata=metadata)
            logger.debug("Appended message to DB for session %s", session_id)
        except Exception as exc:
            logger.error("DB failed to append message, falling back to in-memory: %s", exc)
            _messages.setdefault(session_id, []).append({
                'role': role,
                'text': text,
                'metadata': metadata or {},
                'timestamp': datetime.utcnow().isoformat() + 'Z',
            })

    @staticmethod
    def append_session_summary(session_id, summary):
        """Append session summary to database, fallback to in-memory store on failure."""
        try:
            MentorRepository.save_session_summary(session_id=session_id, summary=summary)
            logger.debug("Saved session summary to DB for session %s", session_id)
        except Exception as exc:
            logger.error("DB failed to save session summary, falling back to in-memory: %s", exc)
            session = _sessions.setdefault(session_id, {})
            session['summary'] = summary
            session['updated_at'] = datetime.utcnow().isoformat() + 'Z'

    @staticmethod
    def get_session(session_id):
        """Retrieve session from database, fallback to in-memory store on failure or if not found."""
        try:
            session_data = MentorRepository.get_session(session_id)
            if session_data:
                # If found in DB, return it
                return session_data
        except Exception as exc:
            logger.error("DB failed to retrieve session, trying in-memory: %s", exc)

        # Fallback to in-memory store
        return {
            'session_id': session_id,
            'messages': _messages.get(session_id, []),
            'summary': _sessions.get(session_id, {}).get('summary', {}),
        }

    @staticmethod
    def append_feedback(session_id, user_id, message, rating):
        """Append feedback to database, fallback to in-memory store on failure."""
        try:
            MentorRepository.append_feedback(session_id=session_id, user_id=user_id, message=message, rating=rating)
            logger.debug("Saved feedback to DB for session %s", session_id)
        except Exception as exc:
            logger.error("DB failed to append feedback, falling back to in-memory: %s", exc)
            _feedback.setdefault(session_id, []).append({
                'user_id': user_id,
                'message': message,
                'rating': rating,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
            })

    @staticmethod
    def summarize_conversation(session_id):
        """Summarize conversation using database messages, fallback to in-memory on failure."""
        try:
            summary = MentorRepository.summarize_conversation(session_id)
            if summary:
                return summary
        except Exception as exc:
            logger.error("DB failed to summarize conversation, trying in-memory: %s", exc)

        # Fallback to in-memory store
        messages = _messages.get(session_id, [])[-20:]
        return ' '.join([m['text'] for m in messages])

    @staticmethod
    def get_memory_value(session_id, key):
        """Get memory value from database, fallback to in-memory on failure."""
        try:
            val = MentorRepository.get_memory_value(session_id, key)
            if val is not None:
                return val
        except Exception as exc:
            logger.error("DB failed to read memory key %s, trying in-memory: %s", key, exc)

        return _memories.get((session_id, key))

    @staticmethod
    def save_memory_value(session_id, key, value):
        """Save memory value to database, fallback to in-memory on failure."""
        try:
            MentorRepository.save_memory_value(session_id, key, value)
            logger.debug("Saved memory key %s to DB for session %s", key, session_id)
        except Exception as exc:
            logger.error("DB failed to save memory key %s, falling back to in-memory: %s", key, exc)
            _memories[(session_id, key)] = value


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
