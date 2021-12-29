import json

from flask import Blueprint, request
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import app
from statics import config
from statics import db
from statics.helpers import permissions_checker

api_create = Blueprint("api_create", __name__)


@crossdomain(origin="*", current_app=app)
@api_create.route("/api/content/create/", methods=["POST"])
@login_required
def create_content():
    if not request.args["type"] in config.known_types:
        return {"error": "Unknown type"}, 400

    permission = permissions_checker(current_user, "create", request.args["type"], request.args["location"])
    if not permission:
        return {"error": "missing permissions"}, 403

    elif permission:
        data = {"name": request.args["name"], "location": request.args["location"], "type": request.args["type"]}

        session = db.factory()
        session.add(db.Content(name=data["name"], location=data["location"], type=data["type"], permissions={current_user.email: 'all'}))
        session.commit()
        session.close()

        return {"message": "success"}, 201
    else:
        return permission, 500
