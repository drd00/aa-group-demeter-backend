import sqlite3
import os

def verify_diarytable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'diary.db')):
        init_diarytable()


def init_diarytable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS diary (uid TEXT, date TEXT NOT NULL, calories REAL NOT NULL, protein REAL NOT NULL, fat REAL NOT NULL, carbs REAL NOT NULL, food TEXT NOT NULL, PRIMARY KEY (uid, date, food, calories, protein, fat, carbs))')
    conn.commit()
    conn.close()


def clean_diarytable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS diary')
    conn.commit()
    conn.close()


def get_diary(uid, date):
    verify_diarytable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diary WHERE uid = ? AND date = ?', (uid, date))
    diaryRows = cursor.fetchall()
    conn.close()

    if diaryRows is None:
        return None
    else:
        return diaryRows

def create_diary(uid, date, calories, protein, fat, carbs, food):
    verify_diarytable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    if get_diary(uid, date) is not None:
        return None

    cursor.execute('INSERT INTO diary (uid, date, calories, protein, fat, carbs, food) VALUES (?, ?, ?, ?, ?, ?, ?)', (str(uid), str(date), float(calories), float(protein), float(fat), float(carbs), str(food)))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid


def create_entry(uid, date, calories, protein, fat, carbs, food):
    verify_diarytable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'diary.db'))
    cursor = conn.cursor()
    cursor.execute('INSERT INTO diary (uid, date, calories, protein, fat, carbs, food) VALUES (?, ?, ?, ?, ?, ?, ?)', (str(uid), str(date), float(calories), float(protein), float(fat), float(carbs), str(food)))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid
