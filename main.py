import flask
from flask import render_template, request

from globals import app
from helpers import init
from routes import user
from routes.api_interact import api_interact
from routes.api_create import api_create
from routes.api_get import api_get
from routes.api_moderate import api_moderate
from routes.permissions import api_permissions
from statics import config

app.debug = True

init.init_db()

app.register_blueprint(user.user_management)
app.register_blueprint(api_get)
app.register_blueprint(api_create)
app.register_blueprint(api_permissions)
app.register_blueprint(api_moderate)
app.register_blueprint(api_interact)

@app.errorhandler(404)
def react(*args, **kwargs):
    if request.path.startswith("/api/"):
        return "Endpoint not found", 404
    return app.send_static_file("index.html")

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

    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

if __name__ == "__main__":
    app.run("0.0.0.0", config.port)
