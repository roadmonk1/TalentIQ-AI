import logging
from datetime import datetime
import uuid
from app import db

logger = logging.getLogger('app.mentor.mission_repository')


class MissionRepository:
    @staticmethod
    def get_user_missions(user_id):
        """Fetch all missions for a user, mapped to frontend-expected goal dictionary format."""
        try:
            from app.mentor.models import Mission

            missions = Mission.query.filter_by(user_id=user_id).order_by(Mission.created_at.asc()).all()
            
            # Map database models to frontend-compatible dictionaries
            mapped = []
            for m in missions:
                progress = 0.0
                if m.status == 'completed':
                    progress = 1.0
                elif m.status == 'accepted':
                    progress = 0.5

                mapped.append({
                    'id': str(m.id),
                    'title': m.title,
                    'description': m.description or '',
                    'progress': progress,
                    'status': m.status,
                    'schedule': m.schedule or {},
                    'created_at': m.created_at.isoformat() + 'Z' if m.created_at else None
                })
            return mapped
        except Exception as exc:
            logger.error("Failed to fetch missions for user %s: %s", user_id, exc)
            return []

    @staticmethod
    def create_mission(user_id, title, description=None, status='pending', session_id=None, schedule=None, due_date=None):
        """Create and persist a new mission."""
        try:
            from app.mentor.models import Mission

            mission = Mission(
                user_id=user_id,
                session_id=session_id,
                title=title,
                description=description,
                status=status,
                schedule=schedule,
                due_date=due_date
            )
            db.session.add(mission)
            db.session.commit()
            logger.info("Created mission '%s' for user %s", title, user_id)
            return mission
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to create mission '%s' for user %s: %s", title, user_id, exc)
            raise exc

    @staticmethod
    def update_mission_status(mission_id, status):
        """Update a mission's status, setting completed_at if status becomes completed."""
        try:
            from app.mentor.models import Mission

            # Convert string ID to UUID object if it's a valid UUID string
            try:
                m_id = uuid.UUID(mission_id) if isinstance(mission_id, str) else mission_id
            except ValueError:
                m_id = mission_id

            mission = Mission.query.filter_by(id=m_id).first()
            if not mission:
                logger.warning("Mission not found with ID %s", mission_id)
                return False

            mission.status = status
            if status == 'completed':
                mission.completed_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to update status for mission %s: %s", mission_id, exc)
            raise exc

    @staticmethod
    def accept_all_pending(user_id):
        """Mark all pending missions for a user as accepted."""
        try:
            from app.mentor.models import Mission

            pending = Mission.query.filter_by(user_id=user_id, status='pending').all()
            for m in pending:
                m.status = 'accepted'
            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to accept pending missions for user %s: %s", user_id, exc)
            raise exc
