from dataclasses import dataclass

PROMPT_VERSION = '1.0'


@dataclass
class Prompt:
    system_prompt: str
    context: str
    user_prompt: str
    version: str = PROMPT_VERSION


class PromptManager:
    @staticmethod
    def system_prompt(mode: str):
        base = (
            'You are TalentIQ AI Mentor, a career coach for ambitious professionals. '
            'Use deterministic resume and career intelligence outputs from TalentParse and TalentCore. '
            'You must explain every recommendation, generate missions, weekly learning plans, and answer questions conversationally.'
        )
        if mode == 'Interview':
            return base + ' Focus on interview preparation, mock interviewer guidance, and behavioral coaching.'
        if mode == 'Learning':
            return base + ' Focus on personalized learning plans and study habits.'
        if mode == 'Motivation':
            return base + ' Focus on motivation, confidence, and next-best-action encouragement.'
        return base

    @staticmethod
    def context_builder(context):
        blocks = [
            f"TARGET_CAREER: {context.target_career}",
            f"CAREER_DNA: {context.career_dna}",
            f"RESUME_HEALTH: {context.resume_health}",
            f"SKILL_GAPS: {context.skill_gaps}",
            f"CAREER_SCORE: {context.career_score}",
            f"RESUME_SCORE: {context.resume_score}",
            f"ATS_SCORE: {context.ats_score}",
            f"WEEKLY_GOALS: {context.weekly_goals}",
            f"MISSION_HISTORY: {context.mission_history}",
            f"PROGRESS: {context.progress}",
            f"PREFERRED_LEARNING_STYLE: {context.preferred_learning_style}",
            f"AVAILABLE_STUDY_TIME: {context.available_study_time}",
        ]
        return '\n'.join(blocks)

    @staticmethod
    def career_prompt(message: str):
        return f"Career Mentor Request:\n{message}\nProvide coaching, missions, and explanations."

    @staticmethod
    def mission_prompt(message: str):
        return f"Mission Generation Request:\n{message}\nReturn a set of daily missions and weekly learning actions."

    @staticmethod
    def interview_prompt(message: str):
        return f"Interview Mentor Request:\n{message}\nProvide mock interview guidance, feedback, and reasoning."

    @staticmethod
    def compose(mode: str, context, message: str):
        system = PromptManager.system_prompt(mode)
        built_context = PromptManager.context_builder(context)
        if mode == 'Interview' or mode == 'Mock Interview':
            user_prompt = PromptManager.interview_prompt(message)
        elif mode == 'Learning':
            user_prompt = PromptManager.mission_prompt(message)
        else:
            user_prompt = PromptManager.career_prompt(message)
        return Prompt(system_prompt=system, context=built_context, user_prompt=user_prompt)

    @staticmethod
    def parse_response(raw):
        return {
            'assistant_text': raw.get('assistant_text', ''),
            'reasoning': raw.get('reasoning', ''),
            'follow_up_questions': raw.get('follow_up_questions', []),
            'next_best_action': raw.get('next_best_action', ''),
            'confidence': raw.get('confidence', 0.7),
            'citations': raw.get('citations', []),
            'daily_missions': raw.get('daily_missions', []),
            'weekly_plan': raw.get('weekly_plan', []),
        }
