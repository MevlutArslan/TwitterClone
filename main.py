from flask import Flask, url_for, render_template, request, redirect
# Response,redirect
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logInStatus = False

# Apparently I need this to run db.create_all() without problems 😅
# from Models import User, Tweet
from Models import User


@app.route('/')
def index():
    return render_template("index.html", logStatus=logInStatus)


@app.route('/LogIn')
def logIn():
    return render_template("logIn.html")


@app.route('/CreateAccount', methods=["GET", "POST"])
def createAccount():
    if request.method == "POST":
        userHandle = request.form["userHandle"]
        userPassword = request.form["password"]
        userDisplayName = request.form["displayName"]
        db.session.add(User(userHandle=userHandle, username=userDisplayName,
                            password=userPassword))
        db.session.commit()
    return redirect("/LogIn")


# snippet to fix static files not updating
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)





if __name__ == "__main__":
    app.run(debug=True)
