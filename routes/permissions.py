import ast

import flask
from flask import Blueprint, request
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import connection_pool, app
from statics import config
from statics.helpers import permissions_checker

api_permissions = Blueprint("api_permissions", __name__)

@crossdomain(origin="*", current_app=app)
@api_permissions.route("/api/permission/user_add_group/")
@login_required
def user_add_group():
    if not permissions_checker(current_user, "groups", "add"):
        return flask.abort(flask.Response(status=401, response="You are not permitted to do that."))

    data = request.args
    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT `groups` FROM {config.Instance.user_instance}_users WHERE `id`='{data['id']}'")
        res = cursor.fetchone()["groups"]
        old_groups = ast.literal_eval(res)
        groups = old_groups

        try:
            groups.append(int(data["group"]))
        except TypeError:
            return flask.abort(flask.Response(response="'group' must be the group id", status=400))

        print(old_groups, groups)

        cursor.execute(f"UPDATE {config.Instance.user_instance}_users SET `groups`='[{', '.join(groups)}]' WHERE `id`='{data['id']}'")

    return {"old_data": old_groups, "new_data": groups}


@crossdomain(origin="*", current_app=app)
@api_permissions.route("/api/permission/user_remove_group/")
@login_required
def user_remove_group():
    if not permissions_checker(current_user, "groups", "remove"):
        return flask.abort(flask.Response(status=401, response="You are not permitted to do that."))

    data = request.args
    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT `groups` FROM {config.Instance.user_instance}_users WHERE `id`='{data['id']}'")
        res = cursor.fetchone()["groups"]
        old_groups = ast.literal_eval(res)
        groups = old_groups

        try:
            groups.remove(int(data["group"]))
        except (TypeError, ValueError):
            return flask.abort(flask.Response(response="'group' must be the group id", status=400))

        print(old_groups, groups)

        cursor.execute(f"UPDATE {config.Instance.user_instance}_users SET `groups`='[{', '.join(groups)}]' WHERE `id`='{data['id']}'")

    return {"old_data": old_groups, "new_data": groups}
