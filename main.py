import time

import pymysql
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required

import api
from crossdomain import crossdomain
from globals import app
from routes import user
from statics import config, init


mysql = pymysql.connect(
    host=config.DB.host,
    port=config.DB.port,
    user=config.DB.user,
    password=config.DB.password,
    db=config.DB.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

init.init_db()

app.register_blueprint(user.user_management)

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


@crossdomain(origin="*", current_app=app)
@app.route("/api/content/create/")
@login_required
def create_content():
    return api.content.create.process(current_user, request)

@crossdomain(origin="*", current_app=app)
@app.route("/api/content/get/")
@login_required
def get_content():
    contents = api.content.get.process(current_user, request)

    if isinstance(contents, tuple):
        return contents

    if contents == False:  # do NOT change to if not contents!
        return "Location not found", 404

    if "html" in request.args.keys():
        print("building page for ", request.args["location"])
        contents = [contents[key] for key in contents.keys()]
        return render_template("components/contents.html", contents=contents)

    return contents


@crossdomain(origin="*", current_app=app)
@app.route("/api/content/get_data/")
@login_required
def get_data():
    location = request.args["location"].split("/")[1:-1]

    data = []

    with mysql.cursor() as cursor:
        while location != []:
            print(location)
            l = '/'+'/'.join(location)+'/'
            print(l)
            cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `path`='{l}'")
            data.append(cursor.fetchone())
            location.pop(len(location)-1)

        cursor.close()

    #data.reverse()

    print(data)

    return jsonify(data)

@app.route('/forum/', defaults={'path': ''})
@app.route('/forum/<path:path>/')
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
    app.run("0.0.0.0", config.port)
