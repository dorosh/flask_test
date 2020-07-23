from app import app, db, mail
from app.forms import LinkForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import (
    current_user,
    login_user,
    logout_user,
)
from flask_mail import Message

from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/create_link', methods=['GET', 'POST'])
def create_link():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LinkForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(email=email)
            user.set_token(email)
            db.session.add(user)
            db.session.commit()
        text_msg = f"""
            Login requested for email {user.email},
            unique link is {request.url_root}login/{user.token}
        """
        flash(text_msg)
        with app.app_context():
            msg = Message(
                subject="Magic link !!!",
                sender=app.config.get("MAIL_USERNAME"),
                recipients=[email],
                body=text_msg
            )
            mail.send(msg)

    return render_template('create_link.html', title='Create link', form=form)


@app.route('/login/<token>')
def login(token):
    if current_user.is_authenticated:
        if current_user.token == token:
            current_user.counter += 1
            db.session.add(current_user)
            db.session.commit()
        return redirect(url_for('create_link'))
    if token:
        user = User.query.filter_by(token=token).first()
        if user is None:
            flash('Invalid token')
            return redirect(url_for('index'))
        else:
            user.counter += 1
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('create_link'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
