
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS') or "config.DevelopmentConfig")
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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(128), index=True, unique=True)
    counter = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_token(self, email):
        self.token = generate_password_hash(email)

if __name__ == '__main__':
    app.run()
