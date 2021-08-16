from globals import mysql
from statics.helpers import permissions_checker
import json

from statics import config

def process(current_user, request):
    with mysql.cursor() as cursor:
        location = request.args["location"]
        if not location.endswith("/"):
            location = location + "/"

        if not permissions_checker(current_user, "view", "all", location):
            return "No permission to view this location", 906

        cursor.execute(f"SELECT * FROM {config.Instance.instance}_content WHERE `location`='{location}'")

        content = cursor.fetchall()

        parsed = {}
        for i in range(0, len(content)):
            parsed[i] = content[i]

        return parsed
