from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from store_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

def create_db():
    with app.app_context():
        db.create_all()

create_db()

from store_app import models
from store_app.api.v1 import category, good