from urllib.parse import urlparse, urljoin

from flask import Blueprint, url_for, redirect, render_template, request, flash
from flask_login import current_user, login_required, logout_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

import api
from crossdomain import crossdomain
from globals import app
from statics import config
from statics.forms import LoginForm, RegisterForm

user_management = Blueprint("user", __name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"{config.DB.type}+{config.DB.driver}://{config.DB.user}:{config.DB.password}@" \
                                 f"{config.DB.host}:{config.DB.port}/{config.DB.db}"

db = SQLAlchemy()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = config.Instance.user_instance + "_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    permissions = db.Column(db.Text, default="{}")
    groups = db.Column(db.Text, default="[]")

    def get_id(self):
        return self.username

    is_anonymous = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"
login_manager.session_protection = "strong"
# login_manager.login_message = "Du bist nicht eingeloggt! Bitte gebe deine Logindaten ein. Dann wirst du zum Ziel weitergeleitet."
login_manager.login_message_category = "info"

@login_manager.user_loader
def user_loader(user_id):
    # return User.query.get(user_id)
    user = User.query.filter_by(username=user_id).first()
    if not user:
        user = User.query.filter_by(email=user_id).first()

    return user

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@crossdomain(origin="*", current_app=app)
@user_management.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.is_submitted():
        return api.login.process(form)

    return render_template("login.html", form=form, user=current_user)


@crossdomain(origin="*", current_app=app)
@user_management.route("/logout/", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("home"))


@user_management.route("/register/", methods=["GET", "POST"])
@crossdomain(origin="*", current_app=app)
def register():
    form = RegisterForm()

    if form.is_submitted():
        return api.register.process(form)

    return render_template("register.html", form=form, user=current_user)
