from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)

def create_db():
    with app.app_context():
        db.create_all()
create_db()

from app import models
from app.api.v1.category import api_category
# from app.api.v1.product import api_product
app.register_blueprint(api_category, url_prefix='/api/v1')
# app.register_blueprint(api_product, url_prefix='/api/v1')