from app import app
from db import db
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash



@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password FROM users WHERE username=:name"
    result = db.session.execute(sql, {"name": username})
    user = result.fetchone()

    if not user:
        print("käyttäjää ei löydy")
        return redirect("/")
    if not check_password_hash(user[0], password):
        print("väärä salasana")
        return redirect("/")

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
