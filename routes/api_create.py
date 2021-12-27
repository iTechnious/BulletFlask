import json

import flask
from flask import Blueprint, request
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import connection_pool, app
from statics import config
from statics.helpers import permissions_checker

api_create = Blueprint("api_create", __name__)


@crossdomain(origin="*", current_app=app)
@api_create.route("/api/content/create/", methods=["POST"])
@login_required
def create_content():
    if not request.args["type"] in config.known_types:
        return "Unknown type", 400

    permission = permissions_checker(current_user, "create", request.args["type"], request.args["location"])
    if not permission:
        return "missing permissions", 403

    elif permission:
        data = {"name": request.args["name"], "location": request.args["location"], "type": request.args["type"]}

        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            # ---------------------- category gets created ----------------------
            if request.args["type"] == "category":
                cursor.execute(f"""INSERT INTO {config.Instance.instance}_content (name, location, type, permissions) VALUES ('{data['name']}', '{data['location']}', '{data['type']}', '{json.dumps({current_user.email: 'all'})}')""")
            # ---------------------- thread gets created ----------------------
            elif request.args["type"] == "thread":
                data["content"] = request.args["content"]

                default_permissions = '{"%s": "all"}' % current_user.email
                query = (data['name'], data['location'], data['type'], data["content"], default_permissions)
                print("inserting data: ", query)
                cursor.execute(f"INSERT INTO `{config.Instance.instance}_content` (name, location, type, content, permissions) VALUES (%s, %s, %s, %s, %s)", query)
            else:
                return "Unknown Type", 400

            dest = str(cursor.lastrowid)  # get destination to redirect the client to
            print(dest)

            con.commit()
            con.close()

        return "success", 201
    else:
        return permission, 500
