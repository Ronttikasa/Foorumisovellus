from db import db
from flask import abort, request, session

def get_categories():
    sql = "SELECT id, category_name FROM categories WHERE visible=True"
    result = db.session.execute(sql)
    return result.fetchall()

def get_category_name(category_id: int):
    sql = "SELECT category_name FROM categories WHERE id=:id"
    result = db.session.execute(sql, {"id": category_id})
    return result.fetchone()[0]

def get_threads(category_id: int):
    sql = "SELECT id, topic FROM threads WHERE category_id=:id AND visible=True"
    result = db.session.execute(sql, {"id":category_id})
    return result.fetchall()

def get_header_data(thread_id: int):
    sql = "SELECT C.id, C.category_name, T.topic FROM threads T, categories C " \
        "WHERE T.id=:id AND T.category_id=C.id LIMIT 1"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()

def get_messages(thread_id: int):
    sql = "SELECT M.id, M.content, U.username, U.id AS user_id, M.time, M.first_in_thread \
        FROM messages M, users U WHERE M.thread_id=:id AND M.user_id=U.id AND M.visible=True ORDER BY M.id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def new_message(content: str, thread_id: int):
    if not content or len(content) > 5100:
        return False
    if not thread_id:
        return False
    user_id = session.get("user_id", 0)
    sql = "INSERT INTO messages (content, user_id, time, thread_id, first_in_thread, visible) \
        VALUES (:content, :user_id, NOW(), :thread_id, False, True)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def new_thread(content: str, topic: str, category_id: int):
    user_id = session.get("user_id", 0)
    if not content or not topic or len(content) > 5100 or len(topic) > 100:
        return False
    if not category_id:
        return False

    sql = "INSERT INTO threads (topic, category_id, visible) \
        VALUES (:topic, :category, True)"
    db.session.execute(sql, {"topic":topic, "category":category_id})
    
    sql = "SELECT MAX(id) FROM threads"
    thread_id = db.session.execute(sql).fetchone()[0]

    sql = "INSERT INTO messages (content, user_id, thread_id, first_in_thread, time, visible) \
        VALUES (:content, :user_id, :thread_id, TRUE, NOW(), True)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def delete_message(msg_id: int):
    sql = "UPDATE messages SET visible=False WHERE id=:id AND first_in_thread=False"
    result = db.session.execute(sql, {"id":msg_id})
    db.session.commit()
    return result.rowcount

def get_newest_message_category(category_id: int):
    sql = "SELECT M.id, M.time FROM messages M, threads T \
        WHERE T.category_id=:category_id ORDER BY M.id DESC LIMIT 1"
    result = db.session.execute(sql, {"category_id":category_id})
    return result.fetchone()

def get_newest_message_thread(thread_id: int):
    sql = "SELECT M.id, U.username, M.time FROM messages M, users U \
        WHERE M.thread_id=:thread_id AND U.id=M.user_id ORDER BY M.id DESC LIMIT 1"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()