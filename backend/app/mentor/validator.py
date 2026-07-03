class ResponseValidator:
    @staticmethod
    def validate(response):
        if not response.get('assistant_text'):
            raise ValueError('Mentor response missing assistant_text')
        validated = {
            'assistant_text': response['assistant_text'],
            'reasoning': response.get('reasoning', ''),
            'follow_up_questions': response.get('follow_up_questions', []),
            'next_best_action': response.get('next_best_action', ''),
            'confidence': response.get('confidence', 0.0),
            'citations': response.get('citations', []),
            'daily_missions': response.get('daily_missions', []),
            'weekly_plan': response.get('weekly_plan', []),
        }
        return validated
