from app import app
from db import db
from flask import render_template, request, redirect, session, abort
import users


@app.route("/")
def index():
    sql = "SELECT id, category_name FROM categories"
    result = db.session.execute(sql)
    categories = result.fetchall()
    return render_template("index.html", categories=categories)

@app.route("/category/<int:id>")
def category(id):
    # TODO: check if user has the privilege to view category
    
    sql = "SELECT id, header FROM threads WHERE category_id=:id"
    result = db.session.execute(sql, {"id":id})
    threads = result.fetchall()
    return render_template("category.html", threads=threads, category_id=id)

@app.route("/thread/<int:id>")
def thread(id):
    sql = "SELECT C.id, C.category_name, T.header FROM threads T, categories C " \
        "WHERE T.id=:id AND T.category_id=C.id LIMIT 1"
    result = db.session.execute(sql, {"id":id})
    header_data = result.fetchone()

    sql = "SELECT M.content, U.username, M.time FROM messages M, users U " \
        "WHERE M.thread_id=:id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()

    return render_template("thread.html", messages=messages, thread_id=id, header_data=header_data)    

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.form["username"].strip()
    password = request.form["password"]
    password_again = request.form["password_again"]

    credentials_ok, error_message = users.check_credentials(username, password, password_again)
    if not credentials_ok:
        return render_template("error.html", message=error_message)

    if not users.register(username, password):
        return render_template("error.html", message="Käyttäjätunnus on jo käytössä.")     
    
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

@app.route("/new_message", methods=["POST"])
def new_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    thread_id = request.form["thread_id"]

    if not content or len(content) > 5100:
        return redirect("/")
    user_id = session.get("user_id", 0)
    sql = "INSERT INTO messages (content, user_id, time, thread_id, first_in_thread) \
        VALUES (:content, :user_id, NOW(), :thread_id, False)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return redirect("/thread/"+str(thread_id))

@app.route("/new_thread", methods=["POST"])
def new_thread():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    header = request.form["header"]
    content = request.form["content"]
    category_id = request.form["category_id"]
    user_id = session.get("user_id", 0)
    
    if not content or not header or len(content) > 5100 or len(header) > 100:
        return redirect("/category"+str(category_id))

    sql = "INSERT INTO threads (header, category_id) \
        VALUES (:header, :category)"
    db.session.execute(sql, {"header":header, "category":category_id})
    
    sql = "SELECT MAX(id) FROM threads"
    thread_id = db.session.execute(sql).fetchone()[0]

    sql = "INSERT INTO messages (content, user_id, thread_id, first_in_thread, time) \
        VALUES (:content, :user_id, :thread_id, TRUE, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()

    return redirect("/category/"+str(category_id))

    
