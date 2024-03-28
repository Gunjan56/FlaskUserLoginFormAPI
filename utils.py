from flask import (Flask, app)
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models.model import db
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
db.init_app(app) 
mail = Mail(app)
migrate = Migrate(app, db)
JWT = JWTManager(app)