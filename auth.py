from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
import os
import shutil
from pathlib import Path

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=["POST"])
def login_post():
    referrer = request.headers.get("Referer")
    
    user_handle = request.form.get('userHandle')
    password = request.form.get('password')
    

    user = User.query.filter_by(user_handle=user_handle).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    user_handle = request.form.get('userHandle')
    display_name = request.form.get('displayName')
    password = request.form.get('password')

    user = User.query.filter_by(user_handle=user_handle).first()

    if user:
        flash('User handle already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(user_handle=user_handle, display_name=display_name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    os.mkdir("./static/user_media/"+user_handle)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/delete_account/<user_id>', methods=["POST"])
@login_required
def delete_account(user_id):
    target_user = User.query.filter_by(id=user_id).first()

    if (target_user.id == current_user.id):
        shutil.rmtree("./static/user_media/"+current_user.user_handle)

        db.session.delete(target_user)
        db.session.commit()

    return redirect(url_for("main.index"))
