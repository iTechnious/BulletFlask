from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user

import api
from crossdomain import crossdomain
from globals import connection_pool, app
from statics import config

api_get = Blueprint("api_get", __name__)

@crossdomain(origin="*", current_app=app)
@app.route("/api/content/get/")
@login_required
def get_content():
    contents, current = api.content.get.process(current_user, request)

    print("get - contents:", contents)
    print("get - current:", current)

    if isinstance(contents, tuple):
        return contents

    if contents == False:  # do NOT change to if not contents!
        return "Location not found", 404

    if "html" in request.args.keys():
        # print("building page for ", request.args["location"])
        contents = [contents[key] for key in contents.keys()]

        print()
        print()
        print(current)

        return render_template("components/contents.html", contents=contents, current=current)

    return contents


@crossdomain(origin="*", current_app=app)
@api_get.route("/api/content/get_data/")
@login_required
def get_data():
    location = request.args["location"]

    # NEEDS PERMISSION SYSTEM!

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        if "breadcrumb" in request.args:
            data = []

            cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{location}'")
            res = cursor.fetchone()
            data.append(res)
            while res["id"] != 0:
                cursor.execute(f"SELECT id, name, location FROM {config.Instance.instance}_content WHERE `id`='{res['location']}'")
                res = cursor.fetchone()
                data.append(res)
                print(data)

            if None in data:
                data.remove(None)

            data = [element for element in data if element["id"] != 0]  # Filter out root entry, which is already in the page

            print("Breadcrumb:", data)
        else:
            cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `id`='{location}'")
            data = cursor.fetchone()

        con.close()

    return jsonify(data)
