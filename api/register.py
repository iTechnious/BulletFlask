from flask_login import login_user
from bcrypt import hashpw, gensalt

from routes.user import user_loader, User, db


def process(form):
    if user_loader(form.username.data) is not None:
        return "Benutzername schon vergeben!", 901
    if user_loader(form.email.data) is not None:
        return "E-Mail bereits registriert!", 902

    salt = gensalt()
    password = hashpw(bytes(form.password.data, "utf-8"), salt).decode("utf-8")
    user = User(username=form.username.data, email=form.email.data, password=password, is_authenticated=True)
    db.session.add(user)
    db.session.commit()

    user = user_loader(form.username.data)
    user.is_authenticated = True
    login_user(user)
    db.session.add(user)
    db.session.commit()

    return "Erfolg", 200
