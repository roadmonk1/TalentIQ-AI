import logging
from app import db

logger = logging.getLogger('app.resume_pipeline.resume_repository')


class ResumeRepository:
    @staticmethod
    def save_profile(user_id, filename, text, parsed_profile, intel, meta, stages):
        """Save resume profile, career score snapshot, and timeline events to DB."""
        try:
            from app.resume_pipeline.models import ResumeProfile, CareerScoreSnapshot, TimelineEvent

            # Remove existing profiles for this user to keep only the latest one
            existing = ResumeProfile.query.filter_by(user_id=user_id).all()
            for ep in existing:
                db.session.delete(ep)
            db.session.flush()

            # Create new profile record
            profile = ResumeProfile(
                user_id=user_id,
                source=meta.get('source', 'upload') if isinstance(meta, dict) else 'upload',
                filename=filename,
                raw_text=text,
                parsed_profile=parsed_profile,
                meta_json=meta
            )
            db.session.add(profile)
            db.session.flush()

            # Create career score snapshot
            scores = intel.get('scores', {})
            career_val = scores.get('careerScore', {}).get('value')
            resume_val = scores.get('resumeScore', {}).get('value')
            ats_val = scores.get('atsScore', {}).get('value')

            score_snap = CareerScoreSnapshot(
                profile_id=profile.id,
                career_score=career_val,
                resume_score=resume_val,
                ats_score=ats_val,
                breakdown=intel
            )
            db.session.add(score_snap)

            # Re-insert timeline events for this user
            existing_events = TimelineEvent.query.filter_by(user_id=user_id).all()
            for ee in existing_events:
                db.session.delete(ee)
            db.session.flush()

            if parsed_profile and 'timeline' in parsed_profile:
                for event in parsed_profile['timeline']:
                    evt = TimelineEvent(
                        user_id=user_id,
                        type=event.get('type', 'upload'),
                        payload=event
                    )
                    db.session.add(evt)

            db.session.commit()
            logger.info("Successfully persisted resume profile for user %s to database", user_id)
            return True
        except Exception as exc:
            db.session.rollback()
            logger.exception("Failed to save resume profile to database for user %s", user_id)
            raise exc

    @staticmethod
    def get_latest_profile(user_id):
        """Fetch the latest resume profile and related scores from the DB."""
        try:
            from app.resume_pipeline.models import ResumeProfile, CareerScoreSnapshot, TimelineEvent

            profile = ResumeProfile.query.filter_by(user_id=user_id).order_by(ResumeProfile.created_at.desc()).first()
            if not profile:
                return None

            # Get latest score snapshot
            score_snap = CareerScoreSnapshot.query.filter_by(profile_id=profile.id).order_by(CareerScoreSnapshot.generated_at.desc()).first()
            intel = score_snap.breakdown if score_snap else {}

            # Get timeline events
            events = TimelineEvent.query.filter_by(user_id=user_id).order_by(TimelineEvent.occurred_at.asc()).all()
            timeline = [evt.payload for evt in events if evt.payload]

            if not timeline and profile.parsed_profile:
                timeline = profile.parsed_profile.get('timeline', [])

            reconstructed_profile = dict(profile.parsed_profile) if profile.parsed_profile else {}
            reconstructed_profile['id'] = profile.user_id
            reconstructed_profile['timeline'] = timeline

            return {
                'profile': reconstructed_profile,
                'intel': intel,
                'meta': profile.meta_json or {},
                'stages': [{'stage': 'Complete', 'timestamp': profile.created_at.isoformat() + 'Z'}]
            }
        except Exception as exc:
            logger.error("Failed to read latest profile from database for user %s: %s", user_id, exc)
            return None
