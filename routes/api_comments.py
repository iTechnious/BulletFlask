from flask import Blueprint, request
from flask_login import login_required, current_user

import helpers.permissions
from crossdomain import crossdomain
from globals import app
from helpers import db

api_moderate = Blueprint("api_comment", __name__)

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/comment/")
@login_required
def comment():
    content_id = request.args["id"]
    content = request.args["content"]

    if helpers.permissions.permission_check(current_user, content_id, "interact", "comment"):
        session = db.factory()
        old = session.query(db.Content).filter_by(id=content_id)[0]

        permissions = old.permissions
        permissions[current_user.email] = "all"

        session.add(db.Content(location=content_id, type="comment", permissions=permissions, content=content))
        session.commit()
        session.close()
    else:
        return {"error": "missing permissions"}, 403
