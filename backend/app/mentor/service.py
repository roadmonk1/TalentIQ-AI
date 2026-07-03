import logging
from datetime import datetime
from app.mentor.context import MentorContextBuilder
from app.mentor.intent import IntentRouter
from app.mentor.prompt import PromptManager
import app.mentor.memory as memory
import app.mentor.adapters as adapters
from app.mentor.validator import ResponseValidator
from app.mentor.formatter import StructuredResponseFormatter

logger = logging.getLogger('app.mentor.service')


class MentorService:
    @staticmethod
    def handle_chat(payload):
        session_id = payload.get('session_id')
        user_id = payload.get('user_id')
        mode = payload.get('mode', 'Career')
        message = payload.get('message', '')
        target_career = payload.get('target_career')

        context = MentorContextBuilder.build(user_id=user_id, session_id=session_id, target_career=target_career, mode=mode)
        context.conversation_summary = memory.summarize_conversation(context.session_id)
        intent = IntentRouter.route(mode=mode, message=message, context=context)

        if intent.is_deterministic:
            # Deterministic intents are executed locally and must not call the LLM/provider
            raw_response = intent.execute(context)
            # Format and validate deterministic response
            response = StructuredResponseFormatter.format(raw_response, source='deterministic')
        else:
            # Compose structured prompt from context and message
            prompt = PromptManager.compose(mode=mode, context=context, message=message)
            provider = adapters.provider_factory()
            try:
                raw_provider_response = provider.chat(prompt)
                # Allow provider to do initial parsing if available, then normalize
                provider_parsed = provider.parse_response(raw_provider_response)
                response = StructuredResponseFormatter.format(provider_parsed, source='provider')
            except Exception as exc:
                # Fallback: do not break the user experience; return deterministic advice
                fallback = IntentRouter.deterministic_career_summary(context)
                response = StructuredResponseFormatter.format(fallback, source='fallback')

        # Validate the structured response before updating memory
        validated = ResponseValidator.validate(response)

        # Append messages only after successful validation
        memory.append_message(session_id=context.session_id, role='user', text=message, metadata={'mode': mode, 'intent': intent.name})
        memory.append_message(session_id=context.session_id, role='assistant', text=validated['assistant_text'], metadata={'mode': mode, 'validated': True})
        memory.append_session_summary(context.session_id, validated)
        return validated

    @staticmethod
    def handle_mission(payload):
        session_id = payload.get('session_id')
        user_id = payload.get('user_id')
        action = payload.get('action', 'generate')
        context = MentorContextBuilder.build(user_id=user_id, session_id=session_id, mode='Learning')
        result = IntentRouter.route_mission(action=action, context=context)
        return result

    @staticmethod
    def get_session(session_id):
        return memory.get_session(session_id)

    @staticmethod
    def refresh_context(payload):
        session_id = payload.get('session_id')
        user_id = payload.get('user_id')
        context = MentorContextBuilder.build(user_id=user_id, session_id=session_id)
        return {'status': 'ok', 'session_id': session_id, 'context': context.to_dict()}

    @staticmethod
    def submit_feedback(payload):
        session_id = payload.get('session_id')
        user_id = payload.get('user_id')
        message = payload.get('message')
        rating = payload.get('rating')
        MemoryStore.append_feedback(session_id, user_id, message, rating)
        return {'status': 'ok'}
