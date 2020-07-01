from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import db
import os
from .models import Tweet, User

tweet_related = Blueprint('tweet_related', __name__)


@tweet_related.route('/tweet')
def tweet():
    return redirect(url_for("main.index"))


@tweet_related.route('/tweet', methods=["POST"])
@login_required
def post_tweet():
    tweet_owner = current_user.id
    tweet_text = request.form.get("tweet_text")

    if tweet_text != "":
        db.session.add(Tweet(tweet_owner_id=tweet_owner, text=tweet_text))
        db.session.commit()

    return redirect(url_for("main.index"))


@tweet_related.route('/tweet/<tweet_id>', methods=["GET"])
def view_tweet_details(tweet_id):
    target_tweet = Tweet.query.get(tweet_id)
    tweet_owner = User.query.get(target_tweet.tweet_owner_id)
    return render_template('tweet_detail.html', tweet=target_tweet, owner=tweet_owner)


@tweet_related.route('/delete_tweet/<tweet_id>', methods=["POST"])
@login_required
def delete_tweet(tweet_id):
    to_delete = Tweet.query.filter_by(id=tweet_id).first()
    if to_delete.tweet_owner_id == current_user.id:
        db.session.delete(to_delete)
        db.session.commit()

    return redirect(url_for("main.index"))


@tweet_related.route('/like/<int:tweet_id>/<action>')
@login_required
def like_tweet(tweet_id, action):
    tweet = Tweet.query.get(tweet_id)
    if action == "like":
        current_user.like_tweet(tweet)
        db.session.commit()
    else:
        current_user.unlike_tweet(tweet)
        db.session.commit()
    return redirect('/')
