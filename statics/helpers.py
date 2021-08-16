import json
from globals import mysql
from statics import config

def permissions_checker(user, group, action, location):
    permissions = json.loads(user.permissions)

    with mysql.cursor() as cursor:
        if cursor.execute(f"SELECT * FROM `{config.Instance.user_instance}_content` WHERE `location`='{location}'") == 0:
            return "Location not found.", 404

        cursor.execute(f'SELECT * FROM {config.Instance.user_instance}_content WHERE `path`="{location}"')
        parent = cursor.fetchone()

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
