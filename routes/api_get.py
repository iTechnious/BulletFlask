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
@api_get.route("/api/content/get/")
@login_required
def get_content():
    location = request.args["location"]

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        q = f"SELECT `id`, `name` FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        res = cursor.fetchone()
        if res is None:
            return flask.abort(flask.Response(response="Location not found", status=404))

        if not permissions_checker(current_user, "view", "all", location):
            return flask.abort(flask.Response(response="No permission to view this location", status=906))

        q = f"SELECT `id`, `name`, `location`, `type` FROM {config.Instance.instance}_content WHERE `location`='{location}'"
        cursor.execute(q)
        content = cursor.fetchall()

        q = f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        current = cursor.fetchone()

        con.close()

    if current is not None:
        try:
            current["permissions"] = json.loads(current["permissions"])[current_user.email]
        except KeyError:
            current["permissions"] = {}

    ################## DONE FETCHING DATA ###################

    if isinstance(content, tuple):  # content is empty
        return content

    if content == False:  # do NOT change to if not content!
        return {"error": "location not found"}, 404

    if "breadcrumb" in request.args:
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            data = []

            cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{request.args['location']}'")
            res = cursor.fetchone()
            data.append(res)
            while res["id"] != 0:
                cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{res['location']}'")
                res = cursor.fetchone()
                data.append(res)

            if None in data:
                data.remove(None)

            # data = [element for element in data if element["id"] != 0]  # Filter out root entry, which is already in the page

    if "version" in request.args.keys():
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {config.Instance.instance}_versions WHERE `id`='{request.args['version']}'")
            version = cursor.fetchone()
            if str(current["id"]) != str(version["content_id"]):
                return {"error": "version ID not found for this post!"}, 409
            current["name"] = version["name"]
            current["content"] = version["content"]
            con.close()
    
    return jsonify({"current": current, "contents": content})

@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/versions/")
@login_required
def versions():
    location = request.args["location"]

    if not permissions_checker(current_user, "view", "all", location):
        return {"error": "missing permissions"}, 403

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM {config.Instance.instance}_versions WHERE `content_id`='{location}' ORDER BY `id` DESC")
        res = cursor.fetchall()

    return jsonify(res)
