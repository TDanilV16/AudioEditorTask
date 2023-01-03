import sqlite3 as sql
import datetime as dt


def get_today_date_and_time():
    now = dt.datetime.now()
    if len(str(now.minute)) > 1:
        today_date_and_time = f"{now.year}/{now.month}/{now.day} " \
                              f"{now.hour}:{now.minute}"
    else:
        today_date_and_time = f"{now.year}/{now.month}/{now.day} " \
                              f"{now.hour}:0{now.minute}"
    return today_date_and_time


def write_history_of_file(input_file_name, action):
    db = sql.connect("history.sqlite")
    time = get_today_date_and_time()
    entity = (time, input_file_name, action)
    cursor = db.cursor()

    cursor.execute("INSERT INTO HISTORY VALUES(?, ?, ?)", entity)

    db.commit()

    db.close()


def get_history_of_file(input_file_name):
    db = sql.connect("history.sqlite")

    cursor = db.cursor()

    cursor\
        .execute("SELECT * FROM HISTORY WHERE file_name = ?;",
                 (input_file_name,))
    record = cursor.fetchall()

    for rec in record:
        print(f"{rec[0]} {rec[1]} {rec[2]}")


def get_all_history():
    db = sql.connect("history.sqlite")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM HISTORY")
    record = cursor.fetchall()

    for rec in record:
        print(f"{rec[0]} {rec[1]} {rec[2]}")
