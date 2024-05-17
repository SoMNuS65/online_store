from marshmallow import Schema, fields, validate

class LoginBodyValidation(Schema):
    email = fields.String(required=True, validate=[validate.Email(), validate.Length(min=1, max=60)])