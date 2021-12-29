import time

import flask
from flask import Blueprint, request
from flask_login import login_required, current_user

from crossdomain import crossdomain
from globals import connection_pool, app, cut_objects
from statics import config
from statics.helpers import permissions_checker

api_moderate = Blueprint("api_moderate", __name__)

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/delete/")
@login_required
def delete_content():
    content_id = request.args["id"]

    if int(content_id) == 0:
        return {"message": "Hey! You are doing that wrong! Don't delete the forum root please...",  "error": "id 0 not deleteable"}, 406

    if permissions_checker(current_user, "moderate", "delete", content_id):
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT `location` FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
            parent_id = cursor.fetchone()["location"]
            cursor.execute(f"DELETE FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")

            con.commit()
            con.close()

            return {"message": "success", "redirect": parent_id}, 200

    else:
        return {"error": "missing permissions"}, 403


@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/cut/")
@login_required
def cut_content():
    content_id = request.args["id"]

    if int(content_id) == 0:
        return {"message": "Hey! You are doing that wrong! Don't move the forum root please...",  "error": "id 0 not moveable"}, 406

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        if permissions_checker(current_user, "moderate", "move", content_id):
            cut_objects[current_user.email] = content_id
            
            return {"message": "success", "redirect": content_id}, 200

        else:
            return {"error": "missing permissions"}, 403
@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/paste/")
@login_required
def paste_content():
    target_id = request.args["target"]

    if current_user.email not in cut_objects.keys():
        return {"error": "no element cut"}, 412

    content_id = cut_objects[current_user.email]

    if int(content_id) == 0:
        return {"message": "Hey! You are doing that wrong! Don't move the forum root please...",  "error": "id 0 not moveable"}, 406

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT `type` FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
        content_type = cursor.fetchone()["type"]
        if permissions_checker(current_user, "create", content_type, target_id):
            cursor.execute(f"UPDATE {config.Instance.instance}_content SET `location`='{target_id}' WHERE `id`='{content_id}'")

            con.commit()
            con.close()

            del cut_objects[current_user.email]

            return {"message": "success", "redirect": content_id}, 200
        else:
            return {"error": "missing permissions"}, 403

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/edit/")
@login_required
def edit():
    content_id = request.args["id"]
    new_name = request.args["name"]
    if "content" in request.args.keys():
        new_content = request.args["content"]
    else:
        new_content = None

    if not permissions_checker(current_user, "moderate", "edit", content_id):
        return {"error": "missing permissions"}, 403

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
        old_data = cursor.fetchone()

        if old_data["type"] in ["category"]:
            new_content = None

        query = (old_data['id'], old_data['name'], old_data['content'], time.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(f"INSERT INTO `{config.Instance.instance}_versions` "
                       f"(content_id, name, content, date) VALUES "
                       f"(%s, %s, %s, %s)", query)

        query = (new_name, new_content, content_id)
        cursor.execute(f"UPDATE `{config.Instance.instance}_content` SET `name`=%s, `content`=%s WHERE `id`=%s", query)
        con.commit()
        con.close()

        return {"message": "success", "redirect": content_id}, 200
