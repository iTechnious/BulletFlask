import flask

from globals import connection_pool
from statics.helpers import permissions_checker, path_parse
import json

from statics import config

def process(current_user, request):
    path = request.args["location"]  # GET argument will be renamed
    if not path.endswith("/"):
        path += "/"
    print("getting content for", path)

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        if path != "/":
            location, current_id = path_parse(path)

            q = f"SELECT `id`, `name` FROM {config.Instance.instance}_content WHERE `id`='{current_id}'"
            cursor.execute(q)
            res = cursor.fetchone()
            print("checking if location is there:", q, res)
            if res is None:
                return flask.abort(flask.Response(response="Location not found", status=404))
        else:
            location = path
            current_id = None

        if not permissions_checker(current_user, "view", "all", path):
            return flask.abort(flask.Response(response="No permission to view this location", status=906))

        q = f"SELECT `id`, `name`, `location`, `type` FROM {config.Instance.instance}_content WHERE `location`='{path}'"
        cursor.execute(q)
        content = cursor.fetchall()
        print("content fetched:", content)
        print("with:", q)

        if current_id is not None:
            q = f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{current_id}'"
            cursor.execute(q)
            current = cursor.fetchone()
            print("current fetched:", current)
            print("with:", q)
        else:
            current = None

        con.close()

    if current is not None:
        try:
            current["permissions"] = json.loads(current["permissions"])[current_user.email]
        except KeyError:
            current["permissions"] = {}

    parsed = {}

    for i in range(0, len(content)):
        parsed[i] = content[i]

    # print(parsed)

    return parsed, current
