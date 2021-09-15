import json

import globals
from globals import connection_pool
from statics import config

def path_parse(path):
    if path != "/":
        path = list(filter(None, path.split("/")))
        location = "/" + "/".join(path[:-1]) + "/"
        location = location.replace("//", "/")
        if len(path) == 1:
            current_id = path[0]
        else:
            current_id = path[-1]
    else:
        location = path
        current_id = location

    return location, current_id

def permissions_checker(user, group, action, path):
    if "admin" in user.groups:
        return True

    print("permission check with:", action, path)
    permissions = json.loads(user.permissions)

    location, current_id = path_parse(path)

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM {config.Instance.user_instance}_content WHERE `location`='{location}'")
        if not cursor.fetchone():
            return "Location not found.", 404

        if location != "/":
            q = f'SELECT * FROM {config.Instance.user_instance}_content WHERE `id`="{current_id}"'
            print(q, location)
            cursor.execute(q)
        else:
            cursor.execute(f'SELECT * FROM {config.Instance.user_instance}_content WHERE `location`="{location}"')

        parent = cursor.fetchone()

        con.close()

    print("permission check on:", parent)

    if parent is not None:
        parent_permissions = json.loads(parent["permissions"])

        try:
            if parent is not None and parent_permissions[user.email][group][action]:
                return True
        except KeyError:
            pass

        for user_group in user.groups:
            try:
                if parent is not None and parent_permissions[user_group][group][action]:
                    return True
            except KeyError:
                pass

    try:
        if permissions[group][action]:
            return True
    except KeyError:
        pass

    return False
