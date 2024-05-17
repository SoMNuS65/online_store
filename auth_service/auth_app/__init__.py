from flask import Flask
from auth_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from redis import Redis

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
jwt = JWTManager(app)
login = LoginManager(app)
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_db():
    with app.app_context():
        db.create_all()

create_db()

from auth_app.api.v1 import auth
from auth_app import models