from app import app
from flask import render_template, request, redirect, session, abort
import users
import messages


@app.route("/")
def index():
    if session.get("username"):
        categories = []

        group_permissions = users.user_in_groups(session.get("user_id"))
        
        for group_id in group_permissions:
            allowed = messages.get_categories_by_group(group_id)
            for category in allowed:
                if category not in categories:
                    categories.append(category)
    else:
        return render_template("index.html")

    return render_template("index.html", categories=categories, groups=group_permissions)

@app.route("/category/<int:id>")
def category(id):
    if session.get("username"):
        if not users.category_access(session.get("user_id"), id):
            return render_template("error.html", message="Ei oikeutta katsella aluetta")
        
        name = messages.get_category_name(id)
        threads = messages.get_threads(id)
    else:
        return index()

    return render_template("category.html", threads=threads, cat_id=id, cat_name=name)

@app.route("/new_category", methods=["POST"])
def new_category():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    if not users.is_admin():
        return render_template("error.html", message="Ei oikeutta luoda uutta aluetta")
    name = request.form["category_name"]
    group = request.form["group"]

    category_added = messages.new_category(name, group)

    if not category_added:
        render_template("error.html", message="Nimi tai käyttäjäryhmän valinta puuttuu")
    
    return index()

@app.route("/thread/<int:id>")
def thread(id):
    if session.get("username"):
        header_data = messages.get_header_data(id)

        if not header_data:
            return render_template("error.html", message="Ketjua ei löytynyt")

        category_id = header_data.id
        user_id = session.get("user_id")

        if not users.category_access(user_id, category_id):
            return render_template("error.html", message="Ei oikeutta katsella viestiketjua")

        msgs = messages.get_messages(id)
        is_admin = users.is_admin()
    else:
        return index()

    return render_template("thread.html", messages=msgs, thread_id=id, header_data=header_data, admin=is_admin)

@app.route("/new_message", methods=["POST"])
def new_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    if not users.category_access(session.get("user_id"), request.form["cat_id"]):
        return render_template("error.html", message="Ei oikeutta kirjoittaa tähän ketjuun")
    content = request.form["content"]
    thread_id = request.form["thread_id"]

    message_posted = messages.new_message(content, thread_id)

    if not message_posted:
        render_template("error.html", message="Viestin lähetys epäonnistui. Viestin tulee olla 1-5000 merkkiä pitkä")

    return redirect("/thread/"+str(thread_id))

@app.route("/new_thread", methods=["POST"])
def new_thread():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    topic = request.form["topic"]
    content = request.form["content"]
    category_id = request.form["category_id"]

    if not users.category_access(session.get("user_id"), category_id):
        return render_template("error.html", message="Ei oikeutta luoda ketjua tälle alueelle")
    
    thread_posted, thread_id = messages.new_thread(content, topic, category_id)

    if not thread_posted:
        return render_template("error.html", message="Ketjun luominen ei onnistunut. Otsikon tulee olla 1-100 merkkiä ja viestin 1-5000 merkkiä pitkä.")

    return redirect("/thread/"+str(thread_id))

@app.route("/delete", methods=["POST"])
def delete_message():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)
    
    message_id = request.form["msg_id"]
    user_id = int(request.form["user_id"])
    thread_id = request.form["thread_id"]

    if session["user_id"] == user_id or users.is_admin():
        msg_deleted = messages.delete_message(message_id)

    if not msg_deleted:
        return render_template("error.html",
            message="Lol yritit nokkelasti poistaa ketjun ensimmäisen viestin mutta etpä voi :P")

    return redirect("/thread/"+str(thread_id))

@app.route("/delete_thread", methods=["POST"])
def delete_thread():
    if not session["csrf_token"] == request.form["csrf_token"]:
        abort(403)

    thread_id = request.form["thread_id"]
    category_id = request.form["cat_id"]

    if users.is_admin():
        messages.delete_thread(thread_id)

    return redirect("/category/"+str(category_id))

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

    
