from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
import os

main = Blueprint('main', __name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@main.route('/')
def index():
    # if current_user.:
    #     return render_template("explore.html", user=current_user)
    return render_template("index.html")


@main.route('/logged_index')
@login_required
def logged_index():
    return render_template('logged_index.html', user=current_user)


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

    return render_template("upload_profile_image.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def upload_file(request):
    # check if the post request has the file part

    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for("main.upload_profile_picture"))
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for("main.upload_profile_picture"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save("/user_media/" + current_user.user_handle+"/"+filename)
        current_user.profile_picture_url = "/user_media/" + current_user.user_handle+"/"+request.files['file']

