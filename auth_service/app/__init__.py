from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import redis
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)
mail = Mail(app)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def create_db():
    with app.app_context():
        db.create_all()
create_db()

from app import models
from app.api.v1.auth import api
app.register_blueprint(api, url_prefix='/api/v1/auth')
