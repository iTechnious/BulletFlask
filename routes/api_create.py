from flask import Blueprint, request
from flask_login import login_required, current_user

import helpers.permissions
from crossdomain import crossdomain
from globals import app
from helpers import db
from statics import config

api_create = Blueprint("api_create", __name__)


@crossdomain(origin="*", current_app=app)
@api_create.route("/api/content/create/")
@login_required
def create_content():
    if not request.args["type"] in config.known_types:
        return {"error": {"message": "unknown type"}}, 400

    permission = helpers.permissions.permission_check(current_user, request.args["location"], "create", request.args["type"])
    if not permission:
        return {"error": {"message": "missing permissions"}}, 403

    elif permission:
        data = {"name": request.args["name"], "location": request.args["location"], "type": request.args["type"]}

        session = db.factory()
        session.add(db.Content(name=data["name"], location=data["location"], type=data["type"], permissions={current_user.email: 'all'}))
        session.commit()
        session.close()

        return {"success": True, "message": "success"}, 201
    else:
        return permission, 500
