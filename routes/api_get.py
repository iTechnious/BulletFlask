import flask
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

import helpers.permissions
from crossdomain import crossdomain
from globals import app
from helpers import db

api_get = Blueprint("api_get", __name__)

@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/get/")
@login_required
def get_content():
    location = request.args["location"]

    session = db.factory()

    res = session.query(db.Content).filter_by(id=location).first()
    if res is None:
        return {"error": {"message": "location not found"}}, 404

    if not helpers.permissions.permission_check(current_user, location, "view", "all"):
        return {"error": {"message": "missing permissions"}}, 403

    content = session.query(db.Content).filter_by(location=location).all()
    _current = session.query(db.Content).filter_by(id=location).first()

    current = _current

    if current is not None:
        try:
            current.permissions = current.permissions[current_user.email]
        except KeyError:
            current.permissions = {}

    ################## DONE FETCHING DATA ##################
    if isinstance(content, tuple):  # content is empty
        return content

    if content == False:  # do NOT change to if not content!
        return {"error": {"message": "location not found"}}, 404

    ################## UPDATING CONTENT IF VERSION ID IS SPECIFIED ##################
    if "version" in request.args.keys():
        version = session.query(db.Versions).filter_by(id=request.args["verions"]).first()

        if str(current["id"]) != str(version["content_id"]):
            return {"error": {"message": "version id not found for this post!"}}, 409
        current["name"] = version["name"]
        current["content"] = version["content"]

    session.close()

    ################## PARSE SQLA OBJECTS TO JSON ##################
    return jsonify(
        {
            "current": {c.name: getattr(current, c.name) for c in current.__table__.columns},
            "contents": [{c.name: getattr(x, c.name) for c in x.__table__.columns if c.name in ["id", "type", "name"]} for x in content]
         }
    )

@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/breadcrumb/")
@login_required
def breadcrumb():
    data = []
    session = db.factory()

    res = session.query(db.Content).filter_by(id=request.args["location"]).first()
    data.append({c.name: getattr(res, c.name) for c in res.__table__.columns if c.name in ["id", "name", "location"]})
    while res.id != 0:
        res = session.query(db.Content).filter_by(id=res.location).first()
        data.append({c.name: getattr(res, c.name) for c in res.__table__.columns if c.name in ["id", "name", "location"]})

    data.reverse()

    return jsonify(data)

@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/versions/")
@login_required
def versions():
    location = request.args["location"]

    if not helpers.permissions.permission_check(current_user, location, "view", "all"):
        return {"error": {"message": "missing permissions"}}, 403

    session = db.factory()

    res = session.query(db.Versions).filter_by(content_id=location).order_by(db.Versions.id)
    res = reversed(res)

    return jsonify(res)
