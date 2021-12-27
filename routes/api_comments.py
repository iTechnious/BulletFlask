import json
import time

import flask
from flask import Blueprint, request
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import connection_pool, app, cut_objects
from statics import config
from statics.helpers import permissions_checker

api_moderate = Blueprint("api_comment", __name__)

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/comment/")
@login_required
def comment():
    content_id = request.args["id"]
    content = request.args["content"]

    if permissions_checker(current_user, "interact", "comment", content_id):
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
            old = cursor.fetchone()

            old["permissions"] = json.loads(old["permissions"])
            old["permissions"][current_user.email] = "all"
            query = (content_id, "comment", old["permissions"], content)
            cursor.execute(f"INSERT INTO `{config.Instance.instance}_content` (`location`, `type`, `permissions`, `content`) VALUES (%s, %s, %s, %s)", query)
    else:
        return "missing permissions", 403
