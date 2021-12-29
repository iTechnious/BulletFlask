import ast
import json

from statics import db


def permissions_checker(user, action_group, action, id):
    if "admin" in user.groups:
        return True

    permissions = user.permissions

    session = db.factory()

    parent = session.query(db.Content).filter_by(id=id).first()

    group_permissions = []

    for group_id in ast.literal_eval(user.groups):
        user_group = session.query(db.Groups).filter_by(id=group_id).first()
        group_permissions.append(user_group.permissions)

    session.close()

    if parent is not None:
        parent_permissions = parent.permissions

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

        try:
            if group_permission[action_group][action] == 1 or group_permission[action_group][action]:
                return True
        except KeyError:
            pass

    return False
