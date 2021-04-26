import flask
from flask_login import login_user
from bcrypt import hashpw, gensalt

import main

def process(form):
    print(form.data)
    if main.user_loader(form.username.data) is not None:
        flask.flash("Benutzername schon vergeben!")
        return flask.redirect(flask.url_for("register"))
    if main.user_loader(form.email.data) is not None:
        flask.flash("E-Mail bereits registriert!")
        return flask.redirect(flask.url_for("register"))

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

    return flask.redirect(flask.url_for("index"))
