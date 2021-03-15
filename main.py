import flask
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from bcrypt import checkpw, hashpw, gensalt
from urllib.parse import urlparse, urljoin

from statics import config, init
from statics.forms import *

init.init_db()

app = Flask("FlaskBullet")
app.TEMPLATES_AUTO_RELOAD = True
app.secret_key = config.secret_key
app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"{config.DB.type}+{config.DB.driver}://{config.DB.user}:{config.DB.password}@" \
                                 f"{config.DB.host}:{config.DB.port}/{config.DB.db}"

db = SQLAlchemy()
db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return self.username

    is_anonymous = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.login_message = "Du bist nicht eingeloggt! Bitte gebe deine Logindaten ein. Dann wirst du zum Ziel weitergeleitet."
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
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dash")
@login_required
def dash():
    return "Dashboard"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_loader(form.username.data)
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
                    flask.flash("Es gab ein Problem beim Loginvorgang. Ist der Benutzer aktiv?")
                    return redirect(url_for("login"))

                db.session.add(user)
                db.session.commit()

                destination = flask.request.args.get('next')

                if destination and is_safe_url(destination):
                    return redirect(destination)
                return redirect(url_for("index"))
            else:
                flask.flash("Das Passwort war falsch!")
                return redirect(request.url)

        else:
            flask.flash("Benutzer wurde nicht gefunden!")
            return redirect(request.url)

    if current_user.is_authenticated:
        return redirect(url_for("dash"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(flask.url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if user_loader(form.username.data) is not None:
            flask.flash("Benutzername schon vergeben!")
            return redirect(request.url)
        if user_loader(form.email.data) is not None:
            flask.flash("E-Mail bereits registriert!")
            return redirect(request.url)

        salt = gensalt()
        password = hashpw(bytes(form.password.data, "utf-8"), salt).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=password, is_authenticated=True)
        login_user(user)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("register.html", form=form)


app.run("127.0.0.1", 80)
