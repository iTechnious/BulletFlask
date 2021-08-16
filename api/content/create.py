from globals import mysql
from statics.helpers import permissions_checker
import json

from statics import config


def cleanup_db(cursor):
    for field in ["location", "path"]:
        cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `{field}` NOT LIKE '%/'")
        for element in cursor.fetchall():
            print("adding trailing slash to ", element)
            cursor.execute(f"UPDATE {config.Instance.instance}_content SET `{field}`=CONCAT(`{field}`, '/') WHERE `id`={element['id']}")

    cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `path` IS NULL")
    for element in cursor.fetchall():
        print("adding path for ", element)
        cursor.execute(f"UPDATE {config.Instance.instance}_content SET `path`='{element['location'] + str(element['id']) + '/'}' WHERE `id`={element['id']}")

def process(current_user, request):
    if not request.args["type"] in ["category"]:
        return "Unknown type", 400
    with mysql.cursor() as cursor:
        permission = permissions_checker(current_user, "create", request.args["type"], request.args["location"])

        if not permission:
            return "Du hast keine Berechtigung eine Kategorie zu erstellen.", 906
        elif permission:
            cursor.execute(f"INSERT INTO {config.Instance.instance}_content (name, location, type) VALUES ('{request.args['name']}', '{request.args['location']}', '{request.args['type']}')")

            cleanup_db(cursor)

            mysql.commit()

            return "OK"
        else:
            return permission, 500
