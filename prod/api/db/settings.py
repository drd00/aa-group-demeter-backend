import sqlite3
import os

from default_settings import DEFAULT_SETTINGS

def verify_settingstable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'settings.db')):
        init_settingstable()


def init_settingstable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (uid INTEGER PRIMARY KEY AUTOINCREMENT, calorie_compensation INTEGER NOT NULL, protein_goal INTEGER NOT NULL, display_calories INTEGER NOT NULL, display_protein INTEGER NOT NULL, display_fat INTEGER NOT NULL, display_carbs INTEGER NOT NULL)')
    conn.commit()
    conn.close()


def clean_settingstable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS settings')
    conn.commit()
    conn.close()


def get_settings(uid):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE uid = ?', (uid,))
    settings = cursor.fetchone()
    conn.close()
    if settings:
        return settings
    else:
        return DEFAULT_SETTINGS


def create_settings(uid, calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    if get_settings(uid) is not None:
        return None

    cursor.execute('INSERT INTO settings (calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs) VALUES (?, ?, ?, ?, ?, ?)', (calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid

