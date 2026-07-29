from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.llm import get_db_connection


class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["email"], row["password_hash"])
    return None


def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["email"], row["password_hash"])
    return None


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["email"], row["password_hash"])
    return None


def set_reset_token(user_id, token, expiry):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE id = %s",
        (token, expiry, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_reset_token(token):
    """Returns the user only if the token exists AND has not expired."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE reset_token = %s AND reset_token_expiry > NOW()",
        (token,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["email"], row["password_hash"])
    return None


def update_password(user_id, new_password):
    password_hash = generate_password_hash(new_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_hash = %s, reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
        (password_hash, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, password_hash)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id