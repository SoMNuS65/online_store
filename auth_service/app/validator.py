from marshmallow import Schema, fields, validate

class VerificationValidation(Schema):
    email = fields.String(required=True, validate=[validate.Email(), validate.Length(min=5)])
    otp = fields.String(required=True, validate=[validate.Length(max=6)])

class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    created_date= fields.DateTime()
