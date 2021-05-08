from bcrypt import checkpw, hashpw, gensalt
import flask
from flask_login import login_user

from main import is_safe_url

import main

def process(form):
    user = main.user_loader(form.username.data)
    if user:
        db_pass = "$2b$12$" + "".join(user.password.split("$").pop())
        db_pass = db_pass.encode("utf-8")

        # form_pass = hashpw(form.password.data.encode("utf-8"), salt)
        form_pass = form.password.data
        form_pass = form_pass.encode("utf-8")

        if checkpw(form_pass, db_pass):
            if login_user(user):
                user.is_authenticated = True
            else:
                return "Es gab ein Problem beim Loginvorgang. Ist der Benutzer aktiv?", 903

            main.db.session.add(user)
            main.db.session.commit()

            return "success", 200
        else:
            return "Das Passwort war falsch!", 904

    else:
        return "Benutzer wurde nicht gefunden!", 905
