from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    full_name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))
    role = fields.String(load_default='Student', validate=validate.OneOf(['Student', 'Recruiter', 'Admin']))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RefreshSchema(Schema):
    refresh_token = fields.String(required=True)
