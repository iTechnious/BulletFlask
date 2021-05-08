from urllib.parse import urlparse, urljoin
import gettext
import pymysql

from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

import api
import api.content.create
from statics import config, init
from statics.forms import *
from crossdomain import crossdomain

init.init_db()

mysql = pymysql.connect(
    host=config.DB.host,
    port=config.DB.port,
    user=config.DB.user,
    password=config.DB.password,
    db=config.DB.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

app = Flask("BulletFlask", static_folder='public')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = config.secret_key
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
    permissions = db.Column(db.Text, default="")
    groups = db.Column(db.Text, default="")

    def get_id(self):
        return self.username

    is_anonymous = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
#login_manager.login_message = "Du bist nicht eingeloggt! Bitte gebe deine Logindaten ein. Dann wirst du zum Ziel weitergeleitet."
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

# -------------------- VIEWS ----------------------
@crossdomain(origin="*", current_app=app)
@app.route("/")
def root():
    return redirect(url_for("index"))

@crossdomain(origin="*", current_app=app)
@app.route("/home")
def index():
    return render_template("index.html")


@crossdomain(origin="*", current_app=app)
@app.route("/dash")
@login_required
def dash():
    return "Dashboard"


@crossdomain(origin="*", current_app=app)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.is_submitted():
        return api.login.process(form)

    return render_template("login.html", form=form)


@crossdomain(origin="*", current_app=app)
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
@crossdomain(origin="*", current_app=app)
def register():
    form = RegisterForm()

    if form.is_submitted():
        return api.register.process(form)

    return render_template("register.html", form=form)

@crossdomain(origin="*", current_app=app)
@app.route("/api/content/create")
def create_content():
    return api.content.create(current_user, request)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    Credit: https://stackoverflow.com/a/34067710
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run("127.0.0.1", config.port)
