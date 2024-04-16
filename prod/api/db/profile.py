import sqlite3
import os

def verify_profiletable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'profile.db')):
        init_profiletable()

def init_profiletable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user (uid TEXT PRIMARY KEY, firstName TEXT, lastName TEXT, age INTEGER, weight REAL, goalWeight REAL, height REAL, activityLevel TEXT)')
    conn.commit()
    conn.close()

def clean_profiletable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user')
    conn.commit()
    conn.close()

def get_profile(uid):
    verify_profiletable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE uid = ?', (uid,))
    profileRow = cursor.fetchone()

    conn.close()
    if profileRow is None:
        return None
    else:
        profile = {
            "uid": profileRow['uid'],
            "firstName": profileRow['firstName'],
            "lastName": profileRow['lastName'],
            "age": profileRow['age'],
            "weight": profileRow['weight'],
            "goalWeight": profileRow['goalWeight'],
            "height": profileRow['height'],
            "activityLevel": profileRow['activityLevel']
        }
        return profile

def create_profile(uid, firstname, lastname, age, weight, goalweight, height, activitylevel):
    verify_profiletable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    if get_profile(uid) is not None:
        return None

    cursor.execute('INSERT INTO user (uid, firstName, lastName, age, weight, goalWeight, height, activityLevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (str(uid), str(firstname), str(lastname), int(age), float(weight), float(goalweight), float(height), str(activitylevel)))
    uid = cursor.lastrowid
    conn.commit()
    conn.close()
    return uid


def update_profile(uid, firstname, lastname, age, weight, goalweight, height, activitylevel):
    verify_profiletable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'profile.db'))
    cursor = conn.cursor()
    if get_profile(uid) is None:
        return None

    cursor.execute('UPDATE user SET firstName = ?, lastName = ?, age = ?, weight = ?, goalWeight = ?, height = ?, activityLevel = ? WHERE uid = ?', (firstname, lastname, age, weight, goalweight, height, activitylevel, uid))
    conn.commit()
    conn.close()
    return uid