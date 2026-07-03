import pytest
import uuid
from app import app, db
from app.resume_pipeline.resume_repository import ResumeRepository
from app.mentor.mentor_repository import MentorRepository
from app.mentor.mission_repository import MissionRepository


@pytest.fixture(autouse=True)
def setup_test_context():
    """Ensure tests run within the Flask app context and database tables are ready."""
    with app.app_context():
        db.create_all()
        yield
        # Clean up database after each test to maintain state cleanliness
        db.session.rollback()
        # We can selectively clean up tables if we want, or just let rollback handle transaction changes.
        # Since SQLite dev.sqlite is used, transactions rollback cleans up in-test additions if they are rolled back.
        # But we commit in repositories. So let's delete test rows manually at the end.
        try:
            from app.mentor.models import MentorMessage, MentorMemory, MentorSession, Mission
            from app.resume_pipeline.models import ResumeProfile, CareerScoreSnapshot, TimelineEvent
            
            # Clear test records using specific identifiers
            MentorMessage.query.filter(MentorMessage.session_id.like("test_%")).delete(synchronize_session=False)
            MentorMemory.query.filter(MentorMemory.session_id.like("test_%")).delete(synchronize_session=False)
            Mission.query.filter(Mission.user_id.like("test_%")).delete(synchronize_session=False)
            TimelineEvent.query.filter(TimelineEvent.user_id.like("test_%")).delete(synchronize_session=False)
            
            # For ResumeProfile, Cascade delete will handle CareerScoreSnapshot
            ResumeProfile.query.filter(ResumeProfile.user_id.like("test_%")).delete(synchronize_session=False)
            MentorSession.query.filter(MentorSession.id.like("test_%")).delete(synchronize_session=False)
            db.session.commit()
        except Exception:
            db.session.rollback()


def test_resume_repository():
    user_id = "test_user_123"
    filename = "my_resume.pdf"
    raw_text = "Experienced software engineer with React and Python skills."
    parsed_profile = {
        "contacts": {"email": "test@example.com"},
        "skills": {"React": {"confidence": 0.9}},
        "raw_text": raw_text
    }
    intel = {
        "scores": {
            "careerScore": {"value": 85},
            "resumeScore": {"value": 90},
            "atsScore": {"value": 75}
        }
    }
    meta = {"source": "upload"}
    stages = [{"stage": "Complete", "timestamp": "2026-07-03T12:00:00Z"}]

    with app.app_context():
        # Save profile
        success = ResumeRepository.save_profile(user_id, filename, raw_text, parsed_profile, intel, meta, stages)
        assert success is True

        # Fetch profile
        result = ResumeRepository.get_latest_profile(user_id)
        assert result is not None
        assert result['profile']['contacts']['email'] == "test@example.com"
        assert result['intel']['scores']['careerScore']['value'] == 85
        assert result['meta']['source'] == "upload"


def test_mentor_repository():
    session_id = "test_session_456"
    user_id = "test_user_456"
    
    with app.app_context():
        # Save session summary
        summary = {"career_plan": "Frontend Dev Plan", "daily_missions": []}
        success = MentorRepository.save_session_summary(session_id, summary)
        assert success is True

        # Append messages
        MentorRepository.append_message(session_id, "user", "Hello Coach", {"user_id": user_id})
        MentorRepository.append_message(session_id, "assistant", "Hello! How can I help you today?", {"user_id": user_id})

        # Get session
        session_data = MentorRepository.get_session(session_id)
        assert session_data is not None
        assert session_data['session_id'] == session_id
        assert len(session_data['messages']) == 2
        assert session_data['messages'][0]['text'] == "Hello Coach"
        assert session_data['messages'][1]['role'] == "assistant"
        assert session_data['summary']['career_plan'] == "Frontend Dev Plan"

        # Summarize conversation
        conv_summary = MentorRepository.summarize_conversation(session_id)
        assert "Hello Coach" in conv_summary
        assert "Hello! How can I help you today?" in conv_summary

        # Memory operations
        MentorRepository.save_memory_value(session_id, "profile_snapshot", {"years_exp": 5})
        mem_val = MentorRepository.get_memory_value(session_id, "profile_snapshot")
        assert mem_val is not None
        assert mem_val['years_exp'] == 5

        # Append feedback
        fb_success = MentorRepository.append_feedback(session_id, user_id, "Great advice", 5)
        assert fb_success is True


def test_mission_repository():
    user_id = "test_user_789"
    
    with app.app_context():
        # Create missions
        m1 = MissionRepository.create_mission(user_id, "Mission 1", "Complete resume parsing check", "pending")
        m2 = MissionRepository.create_mission(user_id, "Mission 2", "Review career score breakdowns", "pending")

        assert m1.id is not None
        assert m2.id is not None

        # Fetch missions
        missions = MissionRepository.get_user_missions(user_id)
        assert len(missions) == 2
        assert missions[0]['title'] == "Mission 1"
        assert missions[0]['status'] == "pending"
        assert missions[0]['progress'] == 0.0

        # Update status
        MissionRepository.update_mission_status(str(m1.id), "accepted")
        MissionRepository.update_mission_status(str(m2.id), "completed")

        # Re-fetch and check
        missions_updated = MissionRepository.get_user_missions(user_id)
        # Note: get_user_missions sorts by created_at asc
        assert missions_updated[0]['status'] == "accepted"
        assert missions_updated[0]['progress'] == 0.5
        assert missions_updated[1]['status'] == "completed"
        assert missions_updated[1]['progress'] == 1.0

        # Create another pending and accept all pending
        m3 = MissionRepository.create_mission(user_id, "Mission 3", "Test pending acceptance", "pending")
        MissionRepository.accept_all_pending(user_id)

        missions_final = MissionRepository.get_user_missions(user_id)
        m3_updated = next(m for m in missions_final if m['title'] == "Mission 3")
        assert m3_updated['status'] == "accepted"
