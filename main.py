from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from flask_scss import Scss

import globals
from crossdomain import crossdomain
from globals import app
from routes import user
from routes.api_create import api_create
from routes.api_get import api_get
from routes.api_moderate import api_moderate
from routes.permissions import api_permissions
from statics import config, init

app.testing = True

init.init_db()

app.register_blueprint(user.user_management)
app.register_blueprint(api_get)
app.register_blueprint(api_create)
app.register_blueprint(api_permissions)
app.register_blueprint(api_moderate)

# -------------------- VIEWS ----------------------
@crossdomain(origin="*", current_app=app)
@app.route("/")
def root():
    return redirect(url_for("home"))

@crossdomain(origin="*", current_app=app)
@app.route("/home/")
def home():
    return render_template("index.html", user=current_user)

@crossdomain(origin="*", current_app=app)
@app.route("/dash/")
@login_required
def dash():
    return "Dashboard"

@app.route('/forum/', defaults={'path': ''})
@app.route('/forum/<path:path>/')
@login_required
def forum(path):
    return render_template("forum_page.html", user=current_user)

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
    Scss(app, static_dir="public/materialize", asset_dir="sass/materialize", load_paths=["sass/materialize/components", "sass/materialize/components/forms"])

    try:
        app.run("0.0.0.0", config.port)
    except KeyboardInterrupt:
        globals.connection_pool.close()
