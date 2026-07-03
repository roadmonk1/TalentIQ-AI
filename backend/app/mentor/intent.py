from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    is_deterministic: bool
    execute: callable


class IntentRouter:
    @staticmethod
    def route(mode, message, context):
        lower = message.strip().lower()
        if any(keyword in lower for keyword in ['mission', 'daily', 'goal', 'learn']):
            return Intent(name='generate_mission', is_deterministic=False, execute=lambda ctx: ctx)
        if any(keyword in lower for keyword in ['resume health', 'resume score', 'ats']):
            return Intent(name='query_resume', is_deterministic=True, execute=IntentRouter.deterministic_resume_summary)
        if any(keyword in lower for keyword in ['career dna', 'career score', 'dna']):
            return Intent(name='query_career', is_deterministic=True, execute=IntentRouter.deterministic_career_summary)
        if mode == 'Mock Interview':
            return Intent(name='mock_interview', is_deterministic=False, execute=lambda ctx: ctx)
        return Intent(name='llm_chat', is_deterministic=False, execute=lambda ctx: ctx)

    @staticmethod
    def route_mission(action, context):
        if action == 'generate':
            return {'status': 'ok', 'missions': context.weekly_goals}
        if action == 'accept':
            return {'status': 'ok', 'message': 'Mission accepted'}
        return {'status': 'ok', 'message': 'Action completed'}

    @staticmethod
    def deterministic_resume_summary(context):
        return {
            'assistant_text': f"Your resume health is {context.resume_health.get('value', 0)} and your top skills include {', '.join(context.skills[:5])}.",
            'confidence': 0.9,
            'next_best_action': 'Review your resume skills section with the AI Mentor',
        }

    @staticmethod
    def deterministic_career_summary(context):
        return {
            'assistant_text': f"Your Career DNA is {context.career_dna.get('primary','N/A')} with a career score of {context.career_score.get('value', 0)}.",
            'confidence': 0.9,
            'next_best_action': 'Ask the Mentor for a specific gap to close',
        }
