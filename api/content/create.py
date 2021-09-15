import flask

import globals
from globals import connection_pool
from statics.helpers import permissions_checker
import json

from statics import config


def cleanup_db(cursor):
    for field in ["location", "path"]:
        cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `{field}` NOT LIKE '%/'")
        for element in cursor.fetchall():
            cursor.execute(f"UPDATE {config.Instance.instance}_content SET `{field}`=CONCAT(`{field}`, '/') WHERE `id`={element['id']}")

    cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `path` IS NULL")
    for element in cursor.fetchall():
        cursor.execute(f"UPDATE {config.Instance.instance}_content SET `path`='{element['location'] + str(element['id']) + '/'}' WHERE `id`={element['id']}")

def process(current_user, request):
    # print(request.form)
    if not request.form["type"] in config.known_types:
        return "Unknown type", 400

    permission = permissions_checker(current_user, "create", request.form["type"], request.form["location"])
    if not permission:
        return "Du hast keine Berechtigung eine Kategorie zu erstellen.", 906

    elif permission:
        data = {"name": request.form["name"], "location": request.form["location"], "type": request.form["type"]}

        with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
            # ---------------------- category gets created ----------------------
            if request.form["type"] == "category":
                cursor.execute(f""""INSERT INTO {config.Instance.instance}_content (name, location, type) VALUES ('{data['name']}', '{data['location']}', '{data['type']}')""")
            # ---------------------- thread gets created ----------------------
            elif request.form["type"] == "thread":
                data["content"] = request.form["content"]

                query = (data['name'], data['location'], data['type'], "\n" + data["content"])
                print("inserting data: ", query)
                cursor.execute(f"INSERT INTO `{config.Instance.instance}_content` (name, location, type, content) VALUES (%s, %s, %s, %s)", query)

            dest = data["location"] + str(cursor.lastrowid) + "/"  # get destination to redirect the client to
            print(dest)

            cleanup_db(cursor)

            con.commit()
            con.close()

        return flask.redirect("/forum/"+dest)
    else:
        return permission, 500
