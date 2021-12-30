from flask_scss import Scss

from globals import app
from helpers import init
from routes import user
from routes.api_create import api_create
from routes.api_get import api_get
from routes.api_moderate import api_moderate
from routes.permissions import api_permissions
from statics import config

app.config["environment"] = "development"

init.init_db()

app.register_blueprint(user.user_management)
app.register_blueprint(api_get)
app.register_blueprint(api_create)
app.register_blueprint(api_permissions)
app.register_blueprint(api_moderate)

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


Scss(app, static_dir="public/materialize", asset_dir="sass/materialize", load_paths=["sass/materialize/components", "sass/materialize/components/forms"])

if __name__ == "__main__":
    app.run("0.0.0.0", config.port)
