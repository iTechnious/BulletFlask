import json
from main import mysql

def permissions_checker(user, group, action, location):
    permissions = json.loads(user["permissions"])

    if cursor.execute(f"SELECT * FROM {config.Instance.user_instance}_content WHERE location={location}") == 0:
        return "Location not found.", 404

    parent_location = location.split("/")
    cursor.execute(f'SELECT * FROM {config.Instance.user_instance}_content WHERE location={"".join(parent[:-1])} AND name={parent[-1]}')
    parent = cursor.fetchone()

    if parent["permissions"][user.email][group][action] == True:
        return True

    for user_group in user.groups:
        if parent[permissions][user_group][group][action] == True:
            return True

    if permissions[group][action] == True:
        return True
        
    return False
