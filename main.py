from flask import Flask, url_for, render_template
# Response,redirect
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
db = SQLAlchemy(app)

#Apparently I need this to run db.create_all() without problems 😅
from Models import User, Tweet


@app.route('/')
def index():
    loggedIn = False
    return render_template("index.html", logStatus=loggedIn)

@app.route('/LogIn')
def logIn():
    return render_template("logIn.html")


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
