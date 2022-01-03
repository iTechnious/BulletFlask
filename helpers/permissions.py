from contextlib import suppress

from helpers import db


def permission_merger(permission_set: list):
    permissions = {}
    for set in permission_set:
        for key in set.keys():
            if set[key] == "all":
                permissions[key] = "all"
            ######### Check if all already there #########
            if key not in permissions.keys():
                permissions[key] = set[key]
            else:
                if type(permissions[key]) == list:
                    for x in set[key]:
                        permissions[key].append(x)
                elif permissions[key] != "all":
                    permissions[key] = set[key]

    return permissions

def group_permission_getter(user):
    session = db.factory()

    group_ids = user.groups

    if not type(group_ids) == list:
        return {}

    groups = []
    for group_id in group_ids:
        group = session.query(db.Groups).filter_by(id=group_id).first()
        groups.append(group.permissions)

    return permission_merger(groups)

def user_element_permission_getter(user, element):
    session = db.factory()
    element = session.query(db.Content).filter_by(id=element).first()
    while element.permissions == {}:
        if element.location is None:
            break
        element = session.query(db.Content).filter_by(id=element.location).first()

    ele_permissions = element.permissions
    session.close()

    try:
        return ele_permissions[user.email]
    except:
        return {}

def group_element_permission_getter(user, element):
    session = db.factory()
    element = session.query(db.Content).filter_by(id=element).first()
    while element.permissions == {}:
        if element.location is None:
            break
        element = session.query(db.Content).filter_by(id=element.location).first()

    group_ids = [x for x in element.permissions.keys() if x in [str(y) for y in user.groups]]

    groups = []
    for group_id in group_ids:
        groups.append(element.permissions[group_id])

    return permission_merger(groups)

def element_revoke_getter(user, element):
    session = db.factory()
    element = session.query(db.Content).filter_by(id=element).first()

    revokes = []
    for key in element.deny:
        if key in [str(x) for x in user.groups] or key == user.email:
            revokes.append(element.deny[key])

    return permission_merger(revokes)

def permission_revoker(permissions: dict, denies: dict):
    for key in denies.keys():
        if denies[key] == "all":
            with suppress(KeyError): del permissions[key]
        elif type(denies[key]) == list:
            if key in permissions.keys() and permissions[key] == "all":
                print(f"WARNING: permissions for {key} could not be parsed correctly!"
                      f"Permissions of type 'all' cannot by denied and were thus removed from this query.")
                del permissions[key]
            elif type(permissions[key]) == list:
                for item in denies[key]:
                    with suppress(KeyError): permissions[key].remove(item)

    return permissions

def permission_getter(user, element):
    permissions = [
        group_permission_getter(user),
        user_element_permission_getter(user, element),
        group_element_permission_getter(user, element),
    ]
    if "all" in permissions:
        return "all"
    permissions = permission_merger(permissions)
    permissions = permission_revoker(permissions, element_revoke_getter(user, element))

    return permissions

def permission_check(user, element, group, action):
    permissions = permission_getter(user, element)
    if permissions == "all":
        return True

    if group in permissions.keys():
        if permissions[group] == "all":
            return True
        elif type(permissions[group]) == list:
            if action in permissions[group]:
                return True
    return False
