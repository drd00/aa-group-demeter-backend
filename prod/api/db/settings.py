import sqlite3
import os

def verify_settingstable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'settings.db')):
        init_settingstable()


def init_settingstable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (uid TEXT PRIMARY KEY, calorie_compensation INTEGER NOT NULL, protein_goal INTEGER NOT NULL, display_calories INTEGER NOT NULL, display_protein INTEGER NOT NULL, display_fat INTEGER NOT NULL, display_carbs INTEGER NOT NULL)')
    conn.commit()
    conn.close()


def clean_settingstable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS settings')
    conn.commit()
    conn.close()


def get_settings(uid):
    verify_settingstable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE uid = ?', (uid,))
    settingsRow = cursor.fetchone()

    conn.close()
    if settingsRow is None:
        return None
    else:
        settings = {
            "uid": settingsRow['uid'],
            "calorie_compensation": settingsRow['calorie_compensation'],
            "protein_goal": settingsRow['protein_goal'],
            "display_calories": settingsRow['display_calories'],
            "display_protein": settingsRow['display_protein'],
            "display_fat": settingsRow['display_fat'],
            "display_carbs": settingsRow['display_carbs']
        }
        return settings

def create_settings(uid, calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs):
    verify_settingstable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    if get_settings(uid) is not None:
        return None

    cursor.execute('INSERT INTO settings (uid, calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs) VALUES (?, ?, ?, ?, ?, ?, ?)', (uid, int(calorie_compensation), int(protein_goal), int(display_calories), int(display_protein), int(display_fat), int(display_carbs)))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid


def update_settings(uid, calorie_compensation, protein_goal, display_calories, display_protein, display_fat, display_carbs):
    verify_settingstable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'settings.db'))
    cursor = conn.cursor()
    if get_settings(uid) is None:
        c = create_settings(uid, int(calorie_compensation), int(protein_goal), int(display_calories), int(display_protein), int(display_fat), int(display_carbs))

        if c is not None:
            return uid
    else:
        cursor.execute('UPDATE settings SET calorie_compensation = ?, protein_goal = ?, display_calories = ?, display_protein = ?, display_fat = ?, display_carbs = ? WHERE uid = ?', (int(calorie_compensation), int(protein_goal), int(display_calories), int(display_protein), int(display_fat), int(display_carbs), uid))
        conn.commit()
        conn.close()
        return uid
