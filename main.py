from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/explore')
@login_required
def explore():
    return render_template('explore.html', user=current_user)
