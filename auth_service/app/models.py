from app import db
from uuid import uuid4
from flask_jwt_extended import decode_token

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    created_date = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f'{self.id} User: {self.username}'
    
class Token(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.Integer, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.Integer, nullable=False)

    @staticmethod
    def add_token_to_db(encoded_token, user_identity):
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        expires = decoded_token['exp']
        revoked = False
        _id = str(uuid4())

        db_token = Token(
            id=_id,
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        )
        db.session.add(db_token)
        db.session.commit()

    

