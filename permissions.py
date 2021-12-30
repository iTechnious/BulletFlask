from statics import db

def group_permission_getter(user):
    session = db.factory()

    group_ids = user.groups

    if not type(group_ids) == list:
        return {}

    groups = []
    for group_id in group_ids:
        group = session.query(db.Groups).filter_by(id=group_id).first()
        groups.append(group.permissions)

    permissions = {}

    for group in groups:
        for key in group.keys():
            if group[key] == "all":
                permissions[key] = "all"
            ######### Check if all already there #########
            if key not in permissions.keys():
                permissions[key] = group[key]
            else:
                if type(permissions[key]) == list:
                    for x in group[key]:
                        permissions[key].append(x)
                elif permissions[key] != "all":
                    permissions[key] = group[key]

    return permissions

def user_element_permission_getter(user, element):
    session = db.factory()
    element = session.query(db.Content).filter_by(id=element).first()

    ele_permissions = element.permissions
    session.close()

    try:
        return ele_permissions[user.email]
    except:
        return {}

def group_element_permission_getter(user, element):
    session = db.factory()
    element = session.query(db.Content).filter_by(id=element).first()

    group_ids = [x for x in element.permissions.keys() if x in [str(y) for y in user.groups]]

    groups = []
    for group_id in group_ids:
        groups.append(element.permissions[group_id])

    permissions = {}

    for group in groups:
        for key in group.keys():
            if group[key] == "all":
                permissions[key] = "all"
            ######### Check if all already there #########
            if key not in permissions.keys():
                permissions[key] = group[key]
            else:
                if type(permissions[key]) == list:
                    for x in group[key]:
                        permissions[key].append(x)
                elif permissions[key] != "all":
                    permissions[key] = group[key]

    return permissions

s = db.factory()
user = s.query(db.User).filter_by(email="sonke@itechnious.com").first()


print(group_element_permission_getter(user, 0))
