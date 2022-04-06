from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:name"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False

    session["username"] = username
    session["user_id"] = user[0]
    session["csrf_token"] = token_hex(16)

    return True

def register(username, password, role):
    try:
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) \
            VALUES (:name, :password, :role)"
        db.session.execute(sql, {"name": username, "password": password_hash, "role":role})
        db.session.commit()   
    except Exception:
        return False
    return login(username, password)


def registration_error(username, password, password_again):
    message = ""
    if not username or len(username) > 20:
        message += "Käyttäjätunnuksessa tulee olla 1-20 merkkiä. "
    if not password == password_again:
        message += "Salasanat eivät ole samat. "
    if len(password) < 8:
        message += "Salasana on liian lyhyt."
    return message