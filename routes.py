from app import app
from db import db
from flask import render_template, request, redirect, session, abort
import users
import messages


@app.route("/")
def index():
    categories = messages.get_categories()

    return render_template("index.html", categories=categories)

@app.route("/category/<int:id>")
def category(id):
    # TODO: check if user has the privilege to view category
    
    name = messages.get_category_name(id)
    threads = messages.get_threads(id)

    return render_template("category.html", threads=threads, cat_id=id, cat_name=name)

@app.route("/thread/<int:id>")
def thread(id):
    header_data = messages.get_header_data(id)
    msgs = messages.get_messages(id)

    return render_template("thread.html", messages=msgs, thread_id=id, header_data=header_data)

@app.route("/new_message", methods=["POST"])
def new_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    thread_id = request.form["thread_id"]

    message_posted = messages.new_message(content, thread_id)

    if not message_posted:
        pass
        # TODO: show error message

    return redirect("/thread/"+str(thread_id))

@app.route("/new_thread", methods=["POST"])
def new_thread():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    topic = request.form["topic"]
    content = request.form["content"]
    category_id = request.form["category_id"]
    
    thread_posted = messages.new_thread(content, topic, category_id)

    if not thread_posted:
        pass
        # TODO: show error message

    return redirect("/category/"+str(category_id))

@app.route("/delete", methods=["POST"])
def delete_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    
    message_id = request.form["msg_id"]
    user_id = int(request.form["user_id"])
    thread_id = request.form["thread_id"]

    if session["user_id"] == user_id:
        msg_deleted = messages.delete_message(message_id)

    if not msg_deleted:
        return render_template("error.html",
            message="Lol yritit nokkelasti poistaa ketjun ensimmäisen viestin mutta etpä voi :P")

    return redirect("/thread/"+str(thread_id))



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        password_again = request.form["password_again"]

        credentials_ok, error_message = users.check_credentials(username, password, password_again)
        if not credentials_ok:
            return render_template("error.html", message=error_message)

        if not users.register(username, password):
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä.")

        users.login(username, password)
        
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
    users.logout()
    return redirect("/")

    
