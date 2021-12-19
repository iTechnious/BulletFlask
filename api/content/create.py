import flask

import globals
from globals import connection_pool
from statics.helpers import permissions_checker
import json

from statics import config

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
                cursor.execute(f"""INSERT INTO {config.Instance.instance}_content (name, location, type, permissions) VALUES ('{data['name']}', '{data['location']}', '{data['type']}', '{json.dumps({current_user.email: 'all'})}')""")
            # ---------------------- thread gets created ----------------------
            elif request.form["type"] == "thread":
                data["content"] = request.form["content"]

                default_permissions = '{"%s": "all"}' % current_user.email
                query = (data['name'], data['location'], data['type'], "\n" + data["content"], default_permissions)
                print("inserting data: ", query)
                cursor.execute(f"INSERT INTO `{config.Instance.instance}_content` (name, location, type, content, permissions) VALUES (%s, %s, %s, %s, %s)", query)
            else:
                return flask.abort(400)

            dest = str(cursor.lastrowid)  # get destination to redirect the client to
            print(dest)

            con.commit()
            con.close()

        return flask.redirect("/forum/"+dest)
    else:
        return permission, 500
