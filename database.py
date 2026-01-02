import sqlite3

db = sqlite3.connect("users.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    plan TEXT,
    expiry INTEGER
)
""")
db.commit()


def add_user(user_id, plan, expiry):
    cur.execute(
        "REPLACE INTO users VALUES (?,?,?)",
        (user_id, plan, expiry)
    )
    db.commit()


def get_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cur.fetchone()


def remove_user(user_id):
    cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    db.commit()
