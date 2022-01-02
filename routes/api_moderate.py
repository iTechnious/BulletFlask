import datetime

from flask import Blueprint, request
from flask_login import login_required, current_user

import helpers.permissions
from crossdomain import crossdomain
from globals import app, cut_objects
from helpers import db

api_moderate = Blueprint("api_moderate", __name__)

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/delete/")
@login_required
def delete_content():
    content_id = request.args["id"]

    if int(content_id) == 0:
        return {"error": {"message": "id 0 not deleteable", "frontend": "ID_0_NOT_EDITABLE"}}, 406

    if helpers.permissions.permission_check(current_user, content_id, "moderate", "delete"):
        session = db.factory()

        parent_id = session.query(db.Content).filter_by(id=content_id).first()

        session.delete(session.query(db.Content).filter_by(id=content_id).first())

        session.commit()
        session.close()

        return {"message": "success", "redirect": parent_id}, 200

    else:
        return {"error": {"message": "missing permissions"}}, 403


@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/cut/")
@login_required
def cut_content():
    content_id = request.args["id"]

    if int(content_id) == 0:
        return {"error": {"message": "id 0 not moveable", "frontend": "ID_0_NOT_EDITABLE"}}, 406

    if helpers.permissions.permission_check(current_user, content_id, "moderate", "move"):
        cut_objects[current_user.email] = content_id

        return {"message": "success", "redirect": content_id}, 200

    else:
        return {"error": {"message": "missing permissions"}}, 403

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/paste/")
@login_required
def paste_content():
    target_id = request.args["target"]

    if current_user.email not in cut_objects.keys():
        return {"error": {"message": "no element cut"}}, 412

    content_id = cut_objects[current_user.email]

    if int(content_id) == 0:
        return {"error": {"message": "id 0 not moveable", "frontend": "ID_0_NOT_EDITABLE"}}, 406

    session = db.factory()

    content_type = session.query(db.Content).filter_by(id=content_id).first()["type"]

    if helpers.permissions.permission_check(current_user, target_id, "create", content_type):
        session.query(db.Content).filter_by(id=content_id).first().location = target_id

        session.commit()
        session.close()

        del cut_objects[current_user.email]

        return {"message": "success", "redirect": content_id}, 200
    else:
        return {"error": {"message": "missing permissions"}}, 403

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/edit/")
@login_required
def edit():
    content_id = request.args["id"]
    if int(content_id) == 0:
        return {"error": {"message": "id 0 not editable", "frontend": "ID_0_NOT_EDITABLE"}}, 406

    new_name = request.args["name"]
    if "content" in request.args.keys():
        new_content = request.args["content"]
    else:
        new_content = None

    if not helpers.permissions.permission_check(current_user, content_id, "moderate", "edit"):
        return {"error": {"message": "missing permissions"}}, 403

    session = db.factory()

    old_data = session.query(db.Content).filter_by(id=content_id).first()

    if old_data.type in ["category"]:
        new_content = None

    session.add(db.Versions(content_id=old_data.id,
                            name=old_data.name,
                            content=old_data.content,
                            date=datetime.datetime.now()))

    element = session.query(db.Content).filter_by(id=content_id)
    element.name = new_name
    element.content = new_content

    session.commit()
    session.close()

    return {"message": "success", "redirect": content_id}, 200
