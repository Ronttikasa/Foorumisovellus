from app import app
from db import db
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex



@app.route("/")
def index():
    sql = "SELECT M.content, U.username, M.time FROM messages M, users U " \
        "WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    messages = result.fetchall()
    return render_template("index.html", messages=messages)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]
    role = 1
    
    # TODO username already exists (error handling)
    # TODO error messages in app
    if not username or len(username) > 20:
        print("käyttäjätunnus ei kelpaa")
    elif not password == password_again:
        print("salasanat eroavat")
    elif len(password) < 8:
        print("salasana liian lyhyt")
    else:
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) \
            VALUES (:name, :password, :role)"
        db.session.execute(sql, {"name": username, "password": password_hash, "role":role})
        db.session.commit()        

    return redirect("/")

@app.route("/new_message", methods=["POST"])
def new_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    if not content or len(content) > 1030:
        return redirect("/")
    user_id = session.get("user_id", 0)
    sql = "INSERT INTO messages (content, user_id, time) \
        VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE username=:name"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()

    # TODO error messages in app
    if not user:
        print("käyttäjää ei löydy")
        return redirect("/")
    if not check_password_hash(user[1], password):
        print("väärä salasana")
        return redirect("/")

    session["username"] = username
    session["user_id"] = user[0]
    session["csrf_token"] = token_hex(16)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
