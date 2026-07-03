from dataclasses import dataclass, field
from app.resume_pipeline.service import get_latest_profile
from app.career_intel.service import CareerIntelService


@dataclass
class MentorContext:
    session_id: str
    user_id: str
    target_career: str
    mode: str
    profile_memory: dict = field(default_factory=dict)
    conversation_memory: dict = field(default_factory=dict)
    mission_memory: dict = field(default_factory=dict)
    learning_memory: dict = field(default_factory=dict)
    interview_memory: dict = field(default_factory=dict)
    weekly_goals: list = field(default_factory=list)
    mission_history: list = field(default_factory=list)
    progress: dict = field(default_factory=dict)
    preferred_learning_style: str = 'adaptive'
    available_study_time: str = '3-5 hours/week'
    skills: list = field(default_factory=list)
    resume_health: dict = field(default_factory=dict)
    career_dna: dict = field(default_factory=dict)
    career_score: dict = field(default_factory=dict)
    resume_score: dict = field(default_factory=dict)
    ats_score: dict = field(default_factory=dict)
    skill_gaps: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    job_matches: list = field(default_factory=list)
    timeline: list = field(default_factory=list)
    weekly_plan: list = field(default_factory=list)
    conversation_summary: str = ''

    def to_dict(self):
        return self.__dict__


class MentorContextBuilder:
    @staticmethod
    def build(user_id=None, session_id=None, target_career='default', mode='Career'):
        stored = get_latest_profile(user_id or 'anon') or {}
        profile = stored.get('profile', {})
        intel = stored.get('intel', {})

        from app.mentor.mission_repository import MissionRepository
        try:
            db_missions = MissionRepository.get_user_missions(user_id or 'anon')
        except Exception:
            db_missions = []

        weekly_goals = db_missions if db_missions else profile.get('weekly_goals', [])
        timeline = profile.get('timeline', [])

        context = MentorContext(
            session_id=session_id or 'anon_session',
            user_id=user_id or 'anon',
            target_career=target_career,
            mode=mode,
            profile_memory={'profile_completion': profile.get('profile_completion', 0.0)},
            conversation_memory={'recent': []},
            mission_memory={'accepted': [], 'pending': []},
            learning_memory={'style': 'adaptive', 'available_time': '3-5 hours/week'},
            interview_memory={'history': []},
            weekly_goals=weekly_goals,
            mission_history=timeline,
            progress={'profile_completion': profile.get('profile_completion', 0.0)},
            preferred_learning_style='adaptive',
            available_study_time='3-5 hours/week',
            skills=list(profile.get('skills', {}).keys()),
            resume_health=profile.get('resume_health', {}),
            career_dna=intel.get('careerDNA', {}),
            career_score=intel.get('scores', {}).get('careerScore', {}),
            resume_score=intel.get('scores', {}).get('resumeScore', {}),
            ats_score=intel.get('scores', {}).get('atsScore', {}),
            skill_gaps=intel.get('skillGaps', []),
            recommendations=intel.get('recommendations', []),
            job_matches=intel.get('jobMatches', []),
            timeline=timeline,
            weekly_plan=[],
            conversation_summary='',
        )
        return context
