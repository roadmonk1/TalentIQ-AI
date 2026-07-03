import logging
from datetime import datetime
from app import db

logger = logging.getLogger('app.mentor.mentor_repository')


class MentorRepository:
    @staticmethod
    def get_session(session_id):
        """Retrieve a session, including its message list and summary."""
        try:
            from app.mentor.models import MentorSession, MentorMessage

            session = MentorSession.query.filter_by(id=session_id).first()
            if not session:
                return None

            messages = MentorMessage.query.filter_by(session_id=session_id).order_by(MentorMessage.created_at.asc()).all()
            formatted_messages = [
                {
                    'role': msg.role,
                    'text': msg.text,
                    'metadata': msg.meta or {},
                    'timestamp': msg.created_at.isoformat() + 'Z'
                }
                for msg in messages
            ]

            return {
                'session_id': session.id,
                'messages': formatted_messages,
                'summary': session.summary or {},
            }
        except Exception as exc:
            logger.error("Failed to retrieve mentor session %s: %s", session_id, exc)
            return None

    @staticmethod
    def save_session_summary(session_id, summary):
        """Save/update the summary of a mentor session."""
        try:
            from app.mentor.models import MentorSession

            session = MentorSession.query.filter_by(id=session_id).first()
            if not session:
                session = MentorSession(id=session_id, summary=summary)
                db.session.add(session)
            else:
                session.summary = summary
                session.updated_at = datetime.utcnow()

            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to save session summary for %s: %s", session_id, exc)
            raise exc

    @staticmethod
    def append_message(session_id, role, text, metadata=None):
        """Append a message to a session, creating the session if it doesn't exist."""
        try:
            from app.mentor.models import MentorSession, MentorMessage

            session = MentorSession.query.filter_by(id=session_id).first()
            user_id = None
            if metadata and isinstance(metadata, dict):
                user_id = metadata.get('user_id')

            if not session:
                # auto-create session
                session = MentorSession(id=session_id, user_id=user_id)
                db.session.add(session)
                db.session.flush()
            elif user_id and not session.user_id:
                session.user_id = user_id
                session.updated_at = datetime.utcnow()

            message = MentorMessage(
                session_id=session_id,
                role=role,
                text=text,
                meta=metadata
            )
            db.session.add(message)
            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to append message to session %s: %s", session_id, exc)
            raise exc

    @staticmethod
    def append_feedback(session_id, user_id, message, rating):
        """Store user feedback as a TimelineEvent."""
        try:
            from app.resume_pipeline.models import TimelineEvent

            evt = TimelineEvent(
                user_id=user_id,
                type='feedback',
                payload={
                    'session_id': session_id,
                    'message': message,
                    'rating': rating,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
            )
            db.session.add(evt)
            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to save feedback for session %s: %s", session_id, exc)
            raise exc

    @staticmethod
    def summarize_conversation(session_id):
        """Summarize conversation by joining the last 20 messages."""
        try:
            from app.mentor.models import MentorMessage
            messages = MentorMessage.query.filter_by(session_id=session_id).order_by(MentorMessage.created_at.asc()).all()
            recent = messages[-20:]
            return ' '.join([m.text for m in recent])
        except Exception as exc:
            logger.error("Failed to summarize conversation for session %s: %s", session_id, exc)
            return ''

    @staticmethod
    def get_memory_value(session_id, key):
        """Get stored memory key value."""
        try:
            from app.mentor.models import MentorMemory
            mem = MentorMemory.query.filter_by(session_id=session_id, key=key).first()
            return mem.value if mem else None
        except Exception as exc:
            logger.error("Failed to read memory key %s for session %s: %s", key, session_id, exc)
            return None

    @staticmethod
    def save_memory_value(session_id, key, value):
        """Save/update memory key value."""
        try:
            from app.mentor.models import MentorMemory

            mem = MentorMemory.query.filter_by(session_id=session_id, key=key).first()
            if not mem:
                mem = MentorMemory(session_id=session_id, key=key, value=value)
                db.session.add(mem)
            else:
                mem.value = value
                mem.updated_at = datetime.utcnow()

            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to save memory key %s for session %s: %s", key, session_id, exc)
            raise exc
