import flask
from flask_login import login_user
from bcrypt import hashpw, gensalt

import main

def process(form):
    if main.user_loader(form.username.data) is not None:
        return "Benutzername schon vergeben!", 901
    if main.user_loader(form.email.data) is not None:
        return "E-Mail bereits registriert!", 902

    salt = gensalt()
    password = hashpw(bytes(form.password.data, "utf-8"), salt).decode("utf-8")
    user = main.User(username=form.username.data, email=form.email.data, password=password, is_authenticated=True)
    main.db.session.add(user)
    main.db.session.commit()

    user = main.user_loader(form.username.data)
    user.is_authenticated = True
    login_user(user)
    main.db.session.add(user)
    main.db.session.commit()

    return "Erfolg", 200
