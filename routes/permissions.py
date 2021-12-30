import ast

import flask
from flask import Blueprint, request
from flask_login import login_required, current_user

import helpers.permissions
from crossdomain import crossdomain
from globals import app
from helpers import db

api_permissions = Blueprint("api_permissions", __name__)

@crossdomain(origin="*", current_app=app)
@api_permissions.route("/api/permission/user_add_group/")
@login_required
def user_add_group():
    if not helpers.permissions.permission_check(current_user, 0, "groups", "add"):
        return flask.abort(flask.Response(status=401, response="You are not permitted to do that."))

    data = request.args
    session = db.factory()

    res = session.query(db.User).filter_by(id=data["id"]).first()
    old_groups = ast.literal_eval(res.groups)
    groups = old_groups

    try:
        groups.append(int(data["group"]))
    except TypeError:
        return flask.abort(flask.Response(response="'group' must be the group id", status=400))

    print(old_groups, groups)

    session.query(db.Users).filter_by(id=data["data"]).first().groups = f"[{', '.join(groups)}]"

    session.commit()
    session.close()

    return {"old_data": old_groups, "new_data": groups}


@crossdomain(origin="*", current_app=app)
@api_permissions.route("/api/permission/user_remove_group/")
@login_required
def user_remove_group():
    if not helpers.permissions.permission_check(current_user, 0, "groups", "remove"):
        return flask.abort(flask.Response(status=401, response="You are not permitted to do that."))

    data = request.args
    session = db.factory()

    res = session.query(db.Users).filter_by(id=data["id"]).first()
    old_groups = ast.literal_eval(res.groups)
    groups = old_groups

    try:
        groups.remove(int(data["group"]))
    except (TypeError, ValueError):
        return flask.abort(flask.Response(response="'group' must be the group id", status=400))

    print(old_groups, groups)

    session.query(db.Users).filter_by(id=data["id"]).first().groups = f"[{', '.join(groups)}]"

    session.commit()
    session.close()

    return {"old_data": old_groups, "new_data": groups}
