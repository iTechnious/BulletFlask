import flask

from globals import connection_pool
from statics.helpers import permissions_checker
import json

from statics import config

def process(current_user, request):
    location = request.args["location"]
    print("getting content for", location)

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        q = f"SELECT `id`, `name` FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        res = cursor.fetchone()
        print("checking if location is there:", q, res)
        if res is None:
            return flask.abort(flask.Response(response="Location not found", status=404))

        if not permissions_checker(current_user, "view", "all", location):
            return flask.abort(flask.Response(response="No permission to view this location", status=906))

        q = f"SELECT `id`, `name`, `location`, `type` FROM {config.Instance.instance}_content WHERE `location`='{location}'"
        cursor.execute(q)
        content = cursor.fetchall()
        print("content fetched:", content)
        print("with:", q)

        q = f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{location}'"
        cursor.execute(q)
        current = cursor.fetchone()
        print("current fetched:", q, current)

        con.close()

    if current is not None:
        try:
            current["permissions"] = json.loads(current["permissions"])[current_user.email]
        except KeyError:
            current["permissions"] = {}

    parsed = {}

    for i in range(0, len(content)):
        parsed[i] = content[i]

    return parsed, current
