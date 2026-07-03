from app.mentor.prompt import PromptManager


class StructuredResponseFormatter:
    @staticmethod
    def format(raw, source='provider'):
        """Normalize raw responses from providers or deterministic intents into the
        structured schema expected by the frontend and validator.

        Accepts either raw dicts from providers or internal deterministic intent
        outputs and returns a dict with keys used by ResponseValidator.
        """
        if raw is None:
            return {
                'assistant_text': '',
                'reasoning': '',
                'follow_up_questions': [],
                'next_best_action': '',
                'confidence': 0.0,
                'citations': [],
                'daily_missions': [],
                'weekly_plan': [],
            }

        # If provider already returns the structured fields, use them
        if isinstance(raw, dict) and raw.get('assistant_text'):
            return {
                'assistant_text': raw.get('assistant_text', ''),
                'reasoning': raw.get('reasoning', ''),
                'follow_up_questions': raw.get('follow_up_questions', []),
                'next_best_action': raw.get('next_best_action', ''),
                'confidence': raw.get('confidence', 0.0),
                'citations': raw.get('citations', []),
                'daily_missions': raw.get('daily_missions', []),
                'weekly_plan': raw.get('weekly_plan', []),
            }

        # Fallback: try to let PromptManager parse common shapes (if provider returns nested)
        if isinstance(raw, dict):
            # Some providers wrap the response under data or result keys
            candidate = raw.get('data') or raw.get('result') or raw.get('response') or raw
            if isinstance(candidate, dict) and candidate.get('assistant_text'):
                return StructuredResponseFormatter.format(candidate, source=source)

        # Last-resort: build an assistant_text from any string fields
        if isinstance(raw, str):
            return {
                'assistant_text': raw,
                'reasoning': '',
                'follow_up_questions': [],
                'next_best_action': '',
                'confidence': 0.0,
                'citations': [],
                'daily_missions': [],
                'weekly_plan': [],
            }

        # If we reached here, we couldn't normalize; return an empty safe structure
        return {
            'assistant_text': str(raw)[:1024] if raw is not None else '',
            'reasoning': '',
            'follow_up_questions': [],
            'next_best_action': '',
            'confidence': 0.0,
            'citations': [],
            'daily_missions': [],
            'weekly_plan': [],
        }
