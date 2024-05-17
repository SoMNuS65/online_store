from flask import request, make_response
from auth_app import app, db, r
from auth_app.api.v1.helper import send_error, send_result
from auth_app.validators import LoginBodyValidation
from auth_app.email import send_email
import secrets
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from auth_app.models import Validation, User
import requests
from flask_login import login_user

ACCESS_EXPIRES = timedelta(days=1)
REFRESH_EXPIRES = timedelta(days=5)


@app.route('/api/v1/auth/login', methods=['POST'])
def login_api():
    '''
        Login/Signup API
        Request body:
            email: string, required
        Returns:
    '''
    try:
        json_req = request.get_json()
    except Exception:
        return send_error(message='incorrect json format', code=400)
    
    json_body = {}

    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    not_validate = LoginBodyValidation().validate(data=json_body)
    if not_validate:
        return send_error(message='Incorrect parameters', code = 400)
    
    email = json_body.get('email')
    verification_code = secrets.token_hex(3)
    print(verification_code)

    is_send_code = Validation.query.filter_by(email=email).first()
    if is_send_code:
        is_send_code.otp = verification_code
        is_send_code.created_at = datetime.utcnow()
        db.session.commit()
    else:
        verification = Validation(email=email, otp=verification_code)
        db.session.add(verification)
        db.session.commit()

    send_email('Подтверждение аккаунта', sender=app.config['MAIL_USERNAME'], recipients=email, text_body=f'Код верификации пользователя: {verification_code}')
    
    data = {
        "email" : email,
        'otp' : verification_code
    }
    return send_result(data)

@app.route('/api/v1/auth/confirm', methods=['GET', 'POST'])
def confirm_api():
    try:
        json_req = request.get_json()
    except Exception():
        return send_error('Incorrect json format')
    

    json_body = {}
    for key, value in json_req.items():
        json_body.setdefault(key, value.strip())

    email = json_body.get('email')
    otp = json_body.get('otp')

    validation = Validation.query.filter_by(email=email, otp=otp).first()

    if validation is None:
        return send_error(message='Invalid otp', code=400)
    
    if validation.is_expired():
        return send_error(message='otp is expired', code=400)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES)
    refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES)
    r.set(access_token, user.id, ex=ACCESS_EXPIRES)
    print(User.query.filter_by(id=r.get(access_token)).first())

    response = make_response(send_result({'access_token' : access_token}))

    response.set_cookie('refresh_token', value=refresh_token, httponly=True, secure=True, max_age=REFRESH_EXPIRES.total_seconds())

    db.session.delete(validation)
    db.session.commit()

    return response
    



    
