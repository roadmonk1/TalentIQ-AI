from marshmallow import Schema, fields


class MentorChatSchema(Schema):
    user_id = fields.String(required=True)
    session_id = fields.String(required=False)
    mode = fields.String(required=False)
    message = fields.String(required=True)
    target_career = fields.String(required=False)


class MentorMissionSchema(Schema):
    user_id = fields.String(required=True)
    session_id = fields.String(required=True)
    action = fields.String(required=True)
