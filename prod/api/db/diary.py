import sqlite3
import os

def verify_diarytable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'diary.db')):
        init_diarytable()


def init_diarytable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS diary (uid INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, calories REAL NOT NULL, protein REAL NOT NULL, fat REAL NOT NULL, carbs REAL NOT NULL)')
    conn.commit()
    conn.close()


def clean_diarytable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS diary')
    conn.commit()
    conn.close()


def get_diary(uid, date):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diary WHERE uid = ? AND date = ?', (uid, date))
    diary = cursor.fetchone()
    conn.close()
    return diary


def create_diary(uid, date, calories, protein, fat, carbs):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    if get_diary(uid, date) is not None:
        return None

    cursor.execute('INSERT INTO diary (date, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?)', (date, calories, protein, fat, carbs))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid

