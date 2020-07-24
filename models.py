from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from wsgi import db, login


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
