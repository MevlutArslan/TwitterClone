# from flask import Flask, url_for, render_template, request, redirect, session
# # Response,redirect
# from flask_login import login_user, logout_user, login_required, current_user, LoginManager
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import uuid
# from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationships.db'
# app.config['SECRET_KEY'] = uuid.uuid4().hex
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# # login_manager = LoginManager()
# # login_manager.login_view = 'login'
# # login_manager.init_app(app)

# # session["logInStatus"] = False
# # session["loggedUser"] = None

# # Apparently I need this to run db.create_all() without problems 😅
# # from Models import User, Tweet
# from Models import User


# @app.route('/')
# def logged_out_index():
#     return render_template("index.html", logStatus=False)


# @app.route('/')
# def logged_in_index():
#     return render_template("index.html", logStatus=True, logged_user=session["logged_user_handle"])


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     error = ""
#     if request.method == "POST":
#         userHandle = request.form["userHandle"]
#         password = request.form["password"]

#         userInDatabase = User.query.filter_by(userHandle=userHandle).first()
#         if userInDatabase and check_password_hash(userInDatabase.password, password):    
#             session["logged_user_handle"] = userInDatabase.userHandle
#             return redirect(url_for('logged_in_index'))
#         else:
#             error = "Wrong credientials"
#     return render_template("logIn.html", thrownError=error)


# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         userHandle = request.form["userHandle"]
#         userPassword = request.form["password"]
#         userDisplayName = request.form["displayName"]
#         db.session.add(User(userHandle=userHandle, username=userDisplayName,
#                             password=generate_password_hash(userPassword, method='sha256')))
#         db.session.commit()
#     return redirect("/login")


# # snippet to fix static files not updating
# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)


# def dated_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = os.path.join(app.root_path, endpoint, filename)
#             values['q'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)


# if __name__ == "__main__":
#     app.run(debug=True)
