from flask import Flask, url_for, render_template, request, redirect, session
# Response,redirect
import os
import uuid
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
app.config['SECRET_KEY'] = uuid.uuid4().hex
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# session["logInStatus"] = False
# session["loggedUser"] = None

# Apparently I need this to run db.create_all() without problems 😅
# from Models import User, Tweet
from Models import User


@app.route('/')
def index():
    if session['loggedUserHandle'] != None:
        print(session["loggedUserHandle"])
        return render_template("index.html", logStatus=session["logInStatus"], loggedAccount=session["loggedUserHandle"])
    return render_template("index.html", logStatus=session["logInStatus"])


@app.route('/LogIn', methods=["GET", "POST"])
def logIn():
    error = ""
    if request.method == "POST":
        userHandle = request.form["userHandle"]
        password = request.form["password"]

        userInDatabase = User.query.filter_by(userHandle=userHandle).first()
        print(userInDatabase)
        if(userInDatabase != None):
            if(userInDatabase.password == password):
                session["logInStatus"] = True
                session["loggedUserHandle"] = userInDatabase.userHandle
                return redirect("/")
            else:
                error = "Wrong Password!"
        else:
            error = "Wrong Handle"
    return render_template("logIn.html", thrownError=error)


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
