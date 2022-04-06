from app import app
from db import db
from flask import render_template, request, redirect, session
import users


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
    username = request.form["username"].strip()
    password = request.form["password"]
    password_again = request.form["password_again"]
    role = 1

    error_message = users.registration_error(username, password, password_again)
    if error_message:
        return render_template("error.html", message=error_message)

    if not users.register(username, password, role):
        return render_template("error.html", message="Käyttäjätunnus on jo käytössä.")     
    
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

    if not users.login(username, password):
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana.")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
