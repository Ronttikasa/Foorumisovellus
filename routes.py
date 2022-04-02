from app import app
from db import db
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]
    role = 1
    
    #TODO: errors
    if not username or len(username) > 20:
        print("username not valid")
    elif not password == password_again:
        print("the passwords differ")
    elif len(password) < 8:
        print("password too short")
    else:
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) \
            VALUES (:name, :password, :role)"
        db.session.execute(sql, {"name": username, "password": password_hash, "role":role})
        db.session.commit()        

    return redirect("/")
    
