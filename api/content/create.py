from main import mysql
from statics.helpers import permissions_checker
import json

def process(current_user, request):
    with mysql.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {config.Instance.user_instance}_users WHERE email={current_user.email}")

        user = cursor.fetchone()

        if permissions_checker(cursor, "create", "category", request.data["location"]) == False:
            return "Du hast keine Berechtigung eine Kategorie zu erstellen.", 906
        
        cursor.execute(f"INSERT INTO {config.Instance.instance}_content (name, location, type) VALUES ({request.data['name']}, {request.data['location']}, {request.data['type']})")
        mysql.commit()

        return "OK"
