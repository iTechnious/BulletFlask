import json

import flask
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import connection_pool, app
from statics import config
from statics.helpers import permissions_checker

api_get = Blueprint("api_get", __name__)

@crossdomain(origin="*", current_app=app)
@app.route("/api/content/get/")
@login_required
def get_content():
    contents, current = api_get_content(current_user, request)

    if isinstance(contents, tuple):  # content is empty
        return contents

    if contents == False:  # do NOT change to if not contents!
        return "Location not found", 404

    if "version" in request.args.keys():
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {config.Instance.instance}_versions WHERE `id`='{request.args['version']}'")
            version = cursor.fetchone()
            if str(current["id"]) != str(version["content_id"]):
                return "Version ID not found for this post!", 409
            current["name"] = version["name"]
            current["content"] = version["content"]
            con.close()

    if "html" in request.args.keys():
        # print("building page for ", request.args["location"])
        contents = [contents[key] for key in contents.keys()]

        return render_template("components/contents.html", contents=contents, current=current)

    if "current" in request.args.keys():
        return current
    return contents


@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/get_data/")
@login_required
def get_data():
    location = request.args["location"]

    # NEEDS PERMISSION SYSTEM!

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        if "breadcrumb" in request.args:
            data = []

            cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{location}'")
            res = cursor.fetchone()
            data.append(res)
            while res["id"] != 0:
                cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{res['location']}'")
                res = cursor.fetchone()
                data.append(res)
                print(data)

            if None in data:
                data.remove(None)

            data = [element for element in data if element["id"] != 0]  # Filter out root entry, which is already in the page

            print("Breadcrumb:", data)
        else:
            cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{location}'")
            data = cursor.fetchone()

        con.close()

    return jsonify(data)

@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/versions/")
@login_required
def versions():
    location = request.args["location"]

    if not permissions_checker(current_user, "view", "all", location):
        return "Du hast nicht die nötigen Rechte!", 401

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM {config.Instance.instance}_versions WHERE `content_id`='{location}' ORDER BY `id` DESC")
        res = cursor.fetchall()

    return jsonify(res)

def api_get_content(current_user, request):
    location = request.args["location"]
    print("getting content for", location)

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        q = f"SELECT `id`, `name` FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        res = cursor.fetchone()
        print("checking if location is there:", q, res)
        if res is None:
            return flask.abort(flask.Response(response="Location not found", status=404))

        if not permissions_checker(current_user, "view", "all", location):
            return flask.abort(flask.Response(response="No permission to view this location", status=906))

        q = f"SELECT `id`, `name`, `location`, `type` FROM {config.Instance.instance}_content WHERE `location`='{location}'"
        cursor.execute(q)
        content = cursor.fetchall()
        print("content fetched:", content)
        print("with:", q)

        q = f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        current = cursor.fetchone()
        print("current fetched:", q, current)

        con.close()

    if current is not None:
        try:
            current["permissions"] = json.loads(current["permissions"])[current_user.email]
        except KeyError:
            current["permissions"] = {}

    parsed = {}

    for i in range(0, len(content)):
        parsed[i] = content[i]

    return parsed, current
