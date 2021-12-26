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
    try:
        content_id = request.form["id"]
    except:
        content_id = request.args["id"]

    if int(content_id) == 0:
        return "Hey! You are doing that wrong! Don't delete the forum root please...", 406

    if permissions_checker(current_user, "moderate", "delete", content_id):
        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT `location` FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
            parent_id = cursor.fetchone()["location"]
            cursor.execute(f"DELETE FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")

            con.commit()
            con.close()

            flask.flash("Das Element wurde erfolgreich gelöscht!")
            return flask.redirect("/forum/"+parent_id)

    else:
        return "Du hast nicht die nötigen Rechte!", 401


@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/cut/")
@login_required
def cut_content():
    try:
        content_id = request.form["id"]
    except:
        content_id = request.args["id"]

    if int(content_id) == 0:
        return "Hey! You are doing that wrong! Don't move the forum root please...", 406

    if current_user.email in cut_objects.keys():
        flask.flash("Das neu ausgeschnittene Element hat ein altes ersetzt!")

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        if permissions_checker(current_user, "moderate", "move", content_id):
            cut_objects[current_user.email] = content_id
            flask.flash("Element ausgeschnitten!")
            return flask.redirect("/forum/" + content_id)

        else:
            return "Du hast nicht die nötigen Rechte!", 401
@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/paste/")
@login_required
def paste_content():
    try:
        target_id = request.form["target"]
    except:
        target_id = request.args["target"]

    if current_user.email not in cut_objects.keys():
        flask.flash("Du hast kein Element ausgeschnitten!")
        return "Du hast kein Element ausgeschnitten!", 412

    content_id = cut_objects[current_user.email]

    if int(content_id) == 0:
        return "Hey! You are doing that wrong! Don't move the forum root please...", 406

    if current_user.email not in cut_objects.keys():
        flask.flash("Du hast kein Element ausgeschnitten!")
        return flask.redirect("/forum/")

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT `type` FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
        content_type = cursor.fetchone()["type"]
        if permissions_checker(current_user, "create", content_type, target_id):
            cursor.execute(f"UPDATE {config.Instance.instance}_content SET `location`='{target_id}' WHERE `id`='{content_id}'")

            con.commit()
            con.close()

            del cut_objects[current_user.email]
            flask.flash("Das Element wurde erfolgreich verschoben!")

            return flask.redirect("/forum/"+content_id)
        else:
            return "Du hast nicht die nötigen Rechte!", 401

@crossdomain(origin="*", current_app=app)
@api_moderate.route("/api/content/moderate/edit/")
@login_required
def edit():
    try:
        content_id = request.form["id"]
        new_name = request.form["name"]
        new_content = request.form["content"]
    except:
        content_id = request.args["id"]
        new_name = request.args["name"]
        new_content = request.args["content"]
    new_content = "\n" + new_content

    if not permissions_checker(current_user, "moderate", "edit", content_id):
        return "Du hast nicht die nötigen Rechte!", 401

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM `{config.Instance.instance}_content` WHERE `id`='{content_id}'")
        old_data = cursor.fetchone()

        query = (old_data['id'], old_data['name'], old_data['content'], time.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(f"INSERT INTO `{config.Instance.instance}_versions` "
                       f"(content_id, name, content, date) VALUES "
                       f"(%s, %s, %s, %s)", query)

        query = (new_name, new_content, content_id)
        cursor.execute(f"UPDATE `{config.Instance.instance}_content` SET `name`=%s, `content`=%s WHERE `id`=%s", query)
        con.commit()
        con.close()

        flask.flash("Das Element wurde erfolgreich editiert!")
        return flask.redirect("/forum/" + content_id)
