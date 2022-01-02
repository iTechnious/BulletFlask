from bcrypt import checkpw, gensalt, hashpw
from flask import Blueprint
from flask_login import current_user, login_required, logout_user, LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy

from statics import config
from crossdomain import crossdomain
from globals import app
from helpers.forms import LoginForm, RegisterForm
from helpers.db import Users

db = SQLAlchemy()

class User(Users, db.Model, UserMixin):
    pass


user_management = Blueprint("user", __name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"{config.DB.type}+{config.DB.driver}://{config.DB.user}:{config.DB.password}@" \
                                 f"{config.DB.host}:{config.DB.port}/{config.DB.db}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_message = False

@app.errorhandler(401)
def not_logged_in(e):
    return {"error": {"message": "you are not logged in!"}}, 401


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(email=user_id).first()

    return user

@crossdomain(origin="*", current_app=app)
@user_management.route('/login_valid/', methods=['GET', 'POST'])
def login_valid():
    if current_user.is_authenticated:
        return {"message": "signed in", "user": {"username": current_user.username}}, 202
    else:
        return {"message": "not signed in"}, 204

@crossdomain(origin="*", current_app=app)
@user_management.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return {"message": "Already signed in.", "user": {"username": current_user.username}}, 202

    form = LoginForm()
    if form.is_submitted():
        if form.email.data is None:
            return {"error": {"message": "no credentials included"}}, 400

        user = user_loader(form.email.data)
        if user:
            db_pass = "$2b$12$" + "".join(user.password.split("$").pop())
            db_pass = db_pass.encode("utf-8")

            # form_pass = hashpw(form.password.data.encode("utf-8"), salt)
            form_pass = form.password.data
            form_pass = form_pass.encode("utf-8")

            if checkpw(form_pass, db_pass):
                if login_user(user):
                    user.is_authenticated = True
                else:
                    return {"error": {"message:" "there was a problem loggin you in. is the user active?"}}, 403

                db.session.add(user)
                db.session.commit()

                return {"message": "success", "user": {"username": user.username}}, 200
            else:
                return {"error": {"message": "wrong password", "frontend": "WRONG_PASSWORD"}}, 401

        else:
            return {"error": {"message": "user not found", "frontend": "USER_NOT_FOUND"}}, 404

    return {"error": {"message": "no form recieved"}}, 400


@crossdomain(origin="*", current_app=app)
@user_management.route("/logout/", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return {"message": "success"}, 200


@user_management.route("/register/", methods=["GET", "POST"])
@crossdomain(origin="*", current_app=app)
def register():
    form = RegisterForm()

    if form.is_submitted():
        if user_loader(form.email.data) is not None:
            return {"error": {"message": "email already taken", "frontend": "EMAIL_TAKEN"}}, 409

        salt = gensalt()
        password = hashpw(bytes(form.password.data, "utf-8"), salt).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=password, is_authenticated=True)
        db.session.add(user)
        db.session.commit()

        user = user_loader(form.email.data)
        user.is_authenticated = True
        login_user(user)
        db.session.add(user)
        db.session.commit()

        return {"message": "success", "user": {"username": user.username}}, 200

    return {"error": {"message": "no form recieved"}}, 400
