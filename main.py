from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
import os
from .models import User, Tweet, LikeTweet
from sqlalchemy import desc

main = Blueprint('main', __name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@main.route('/')
def index():
    if current_user.is_authenticated:
        all_tweets = Tweet.query.order_by(Tweet.date.desc()).all()
        return render_template('logged_index.html', user=current_user, tweets=all_tweets)
    else:
        return render_template("index.html")


@main.route('/upload_profile_picture', methods=["GET", "POST"])
@login_required
def upload_profile_picture():
    if request.method == "POST":
        file = request.files['upload_picture']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("main.upload_profile_picture"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("static/user_media/"+current_user.user_handle, filename))
            current_user.profile_picture_url = "user_media/" + current_user.user_handle+"/"+filename
            db.session.commit()
            return redirect(url_for("main.index"))

    return render_template("upload_profile_image.html")


@main.route('/profile/<user_handle>')
def user_profile(user_handle):
    target_user = User.query.filter_by(user_handle=user_handle).first()
    liked_tweets = LikeTweet.query.filter_by(liked_by=target_user.id).all()

    return render_template('profile.html', user=target_user, liked=liked_tweets)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/follow/<user_id>')
@login_required
def follow_user(user_id):
    referrer = request.headers.get("Referer")

    target_user = User.query.filter_by(id=user_id).first()
    print(target_user)

    if current_user.is_following(target_user):
        current_user.unfollow(target_user)
        db.session.commit()
    else:
        current_user.follow(target_user)
        db.session.commit()

    return redirect(referrer)
