from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
from sqlalchemy.exc import IntegrityError

def login(username, password):
    sql = "SELECT U.id, U.password, G.group_id FROM users U, users_in_groups G \
        WHERE U.username=:name AND U.id=G.user_id ORDER BY G.group_id ASC LIMIT 1"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False

    session["username"] = username
    session["user_id"] = user[0]
    session["role"] = user[2]
    session["csrf_token"] = token_hex(16)

    return True

def logout():
    del session["username"]
    del session["user_id"]
    del session["role"]
    del session["csrf_token"]

def register(username, password):
    try:
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, visible) \
            VALUES (:name, :password, True)"
        db.session.execute(sql, {"name": username, "password": password_hash})

        user_id = db.session.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1").fetchone()[0]

        sql = "INSERT INTO users_in_groups (user_id, group_id, visible) \
            VALUES (:user_id, 2, True)"
        db.session.execute(sql, {"user_id": user_id})
        db.session.commit()
    except IntegrityError:
        return False
    return True

def check_credentials(username, password, password_again):
    message = ""
    if not username or len(username) > 20:
        message += "Käyttäjätunnuksessa tulee olla 1-20 merkkiä. "
    if not password == password_again:
        message += "Salasanat eivät ole samat. "
    if len(password) < 8:
        message += "Salasana on liian lyhyt."
    if not message:
        return True, None
    return False, message