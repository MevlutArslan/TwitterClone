from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import db
import os
from .models import Tweet

tweet_related = Blueprint('tweet_related', __name__)


@tweet_related.route('/tweet')
def tweet():
    return redirect(url_for("main.logged_index"))


@tweet_related.route('/tweet', methods=["POST"])
@login_required
def post_tweet():
    tweet_owner = current_user.id
    tweet_text = request.form.get("tweet_text")

    db.session.add(Tweet(tweet_owner_handle=tweet_owner, text=tweet_text, likes=0))
    db.session.commit()
    return redirect(url_for("main.logged_index"))
