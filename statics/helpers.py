import ast
import json

from globals import connection_pool
from statics import config

"""
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
"""

def permissions_checker(user, action_group, action, id):
    if "admin" in user.groups:
        return True

    permissions = json.loads(user.permissions)

    with connection_pool.connection() as con, con.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM {config.Instance.user_instance}_content WHERE `id`='{id}'")
        location = cursor.fetchone()["location"]

        q = f'SELECT * FROM {config.Instance.user_instance}_content WHERE `id`="{id}"'
        cursor.execute(q)

        parent = cursor.fetchone()
        group_permissions = []

        for group_id in ast.literal_eval(user.groups):
            cursor.execute(f"SELECT * FROM `{config.Instance.user_instance}_groups` WHERE `id`='{group_id}'")
            user_group = cursor.fetchone()
            group_permissions.append(json.loads(user_group["permissions"]))

        con.close()

    if parent is not None:
        parent_permissions = json.loads(parent["permissions"])

        if parent_permissions[user.email] == "all":
            return True

        try:
            if action in parent_permissions[user.email][action_group]:
                return True
        except TypeError:
            pass

        for user_group in user.groups:
            try:
                if action in parent_permissions[user_group][action_group]:
                    return True
            except KeyError:
                pass


    try:
        if permissions[action_group][action]:
            return True
    except KeyError:
        pass

    for group_permission in group_permissions:
        try:
            if group_permission[action_group] == "all":
                return True
        except KeyError:
            pass

        # group_permission = json.loads(group_permission)
        try:
            if group_permission[action_group][action] == 1 or group_permission[action_group][action]:
                return True
        except KeyError:
            pass

    return False
