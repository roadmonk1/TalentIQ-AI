from datetime import datetime


class MentorSession:
    def __init__(self, session_id, user_id, created_at=None):
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow().isoformat() + 'Z'
        self.updated_at = self.created_at
        self.active = True
        self.messages = []
        self.memory = {
            'profile': {},
            'conversation': [],
            'mission': [],
            'learning': [],
            'interview': [],
        }

    def add_message(self, message):
        self.messages.append(message)
        self.updated_at = datetime.utcnow().isoformat() + 'Z'
