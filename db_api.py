import datetime
import sqlite3

connect = sqlite3.connect('db.sqlite')
cursor = connect.cursor()


def add_user_status(user_id, sub_id, data):
    cursor.execute(
        "INSERT INTO USERS_STATUS VALUES(?, ?, ?, ?)",
        (user_id, sub_id, data, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    connect.commit()


def get_user(user_id):
    return cursor.execute("SELECT * FROM USERS_STATUS WHERE user_id = ?", (user_id,)).fetchone()


def get_all_status(user_id):
    return cursor.execute("SELECT * FROM USERS_STATUS where user_id = ?", (user_id,)).fetchall()
