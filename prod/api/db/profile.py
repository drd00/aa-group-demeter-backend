import sqlite3
import os

def verify_profiletable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'profile.db')):
        init_profiletable()

def init_profiletable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user (uid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, age INTEGER, weight REAL, goalweight REAL, height REAL, primarygoal TEXT, activitylevel TEXT)')
    conn.commit()
    conn.close()

def clean_profiletable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user')
    conn.commit()
    conn.close()

def get_profile(uid):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE uid = ?', (uid,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def create_profile(uid, firstname, lastname, age, weight, goalweight, height, primarygoal, activitylevel):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    if get_profile(uid) is not None:
        return None

    cursor.execute('INSERT INTO user (firstname, lastname, age, weight, goalweight, height, primarygoal, activitylevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (firstname, lastname, age, weight, goalweight, height, primarygoal, activitylevel))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid