from flask import Blueprint, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, verify_jwt_in_request, decode_token, jwt_required, get_jwt_identity
from app.api.helper import send_error, send_result, json_parse
from app import mail, app, r, db
from app.validator import VerificationValidation, UserSchema
from app.email import send_email
from app.models import User, Token
from datetime import timedelta, datetime, timezone
from secrets import token_hex

api = Blueprint("auth", __name__)

ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=1)

@api.route('/login', methods=["POST"])
def login():
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)

    email = json_body.get('email')

    if r.get(email) == None:
        otp = token_hex(3)
        send_email(subject='Verification code', recipients=[email], body=otp)
        r.setex(name=email, value=otp, time=timedelta(seconds=90))
        return send_result(message=f'Verification code are sended on {email}')
    
    return send_result(message="Check your email!")



@api.route('/confirm', methods=['POST'])
def confirm():
    try:
        json_req = request.get_json()
    except:
        return send_error(message='Incorrect json format!')
    
    if json_req is None:
        return send_error("Check your json object!")
    
    json_body = json_parse(json_req)

    is_not_validate = VerificationValidation().validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid parameters')
    
    email = json_body.get('email')
    otp = json_body.get('otp')

    is_otp = r.get(email)
    if is_otp is None:
        return send_error(message="Verification code is expired or email didn't try to log in!")

    if is_otp != otp:
        return send_error(message="Incorrect verification code")
    r.delete(email)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, created_date=datetime.now())
        db.session.add(user)
        db.session.commit()
    
    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES)
    refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES)
    Token.add_token_to_db(refresh_token, user.id)

    data = {'access_token' : access_token}
    response = make_response(send_result(data=data))
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    return response


@api.route('/validate', methods=['GET'])
@jwt_required()
def validate_token():
    verify_jwt_in_request()
    return send_result()


@api.route('/refresh', methods=['GET'])
def get_new_tokens():
    refresh_token = request.cookies.get(key="refresh_token")
    if not refresh_token:
        return send_error(message="Missing refresh token", code=401)
    
    decoded_token = decode_token(refresh_token)
    jti = decoded_token['jti']
    user_identity = decoded_token['sub']
    expires = decoded_token['exp']

    db_token = Token.query.filter_by(jti=jti, token_type='refresh', revoked=False).first()
    if not db_token:
        return send_error(message='Invalid refresh token', code=401)
    
    if datetime.now(timezone.utc).timestamp() > expires:
        return send_error(message='Expired refresh token', code=401)
    
    new_access_token = create_access_token(identity=user_identity, expires_delta=ACCESS_EXPIRES)
    new_refresh_token = create_refresh_token(identity=user_identity, expires_delta=REFRESH_EXPIRES)
    
    db_token.revoked = True
    db.session.commit()
    
    Token.add_token_to_db(new_refresh_token, user_identity)
    
    data = {'access_token': new_access_token}
    response = make_response(send_result(data=data, message="Refresh token and access token has been refreshed successfully!"))
    response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True)
    return response


@api.route('/logout', methods=['GET'])
@jwt_required()
def logout_user():
    current_user = get_jwt_identity()
    db.session.query(Token).filter(Token.user_identity==current_user).update({'revoked' : True})
    db.session.commit()
    return send_result(message='You are logged out successfully!')