import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ('APP_SETTINGS') or "config.DevelopmentConfig")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.config.update({
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER') or "dorosshh@gmail.com",
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD') or "FH0llnkjt556HJGHGF556",
})
mail = Mail(app)

from app import models, routes
