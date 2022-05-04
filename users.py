from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
from sqlalchemy.exc import IntegrityError

def login(username: str, password: str):
    sql = "SELECT id, password FROM users \
        WHERE username=:name AND visible=True"
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

def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]

def register(username: str, password: str):
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

def check_credentials(username: str, password: str, password_again: str):
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

def get_groups():
    sql = "SELECT id, group_name FROM groups WHERE visible=True"
    result = db.session.commit(sql).fetchall()
    return result

def user_in_groups(user_id: int):
    sql = "SELECT group_id FROM users_in_groups WHERE user_id=:user_id AND visible=True"
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    groups = []
    for r in result:
        groups.append(r.group_id)
    return groups

def is_admin():
    user_id = session.get("user_id", 0)
    sql = "SELECT user_id FROM users_in_groups WHERE group_id=1 AND user_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()

    if not result:
        return False
    return True

def category_access(user_id: int, category_id: int):
    groups = user_in_groups(user_id)
    for group_id in groups:
        sql = "SELECT 1 FROM category_access WHERE group_id=:group_id AND category_id=:category_id"
        result = db.session.execute(sql, {"group_id":group_id, "category_id":category_id})
        if result.fetchone():
            return True
        continue
    return False