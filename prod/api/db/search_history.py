import sqlite3
import os
import random

'''
    search_history table contains previous search RESULTS returned for a particular user.
    and associated weights corresponding to the search results.
'''

def decay_weight(uid):
    verify_searchtable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE uid = ?', (uid,))
    searchRows = cursor.fetchall()
    for searchRow in searchRows:
        prediction_weight = searchRow['prediction_weight']
        decayed_weight = prediction_weight * 0.9
        cursor.execute('UPDATE search SET prediction_weight = ? WHERE uid = ? AND search = ? AND timestamp = ?', (decayed_weight, uid, searchRow['search'], searchRow['timestamp']))
    conn.commit()
    conn.close()


def clear_low_weight(uid):
    verify_searchtable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE uid = ?', (uid,))
    searchRows = cursor.fetchall()
    for searchRow in searchRows:
        prediction_weight = searchRow['prediction_weight']
        if prediction_weight < 1.0:
            cursor.execute('DELETE FROM search WHERE uid = ? AND search = ? AND timestamp = ?', (uid, searchRow['search'], searchRow['timestamp']))
    conn.commit()
    conn.close()


def verify_searchtable():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'search_history.db')):
        init_searchtable()
    

def init_searchtable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS search (uid TEXT, search TEXT, timestamp TEXT, prediction_weight REAL, attrs TEXT, PRIMARY KEY (uid, search, timestamp))')
    conn.commit()
    conn.close()


def clean_searchtable():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS search')
    conn.commit()
    conn.close()


def get_search_history(uid):
    verify_searchtable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE uid = ? ORDER BY timestamp DESC', (uid,))
    searchRows = cursor.fetchall()
    conn.close()

    search_history = []
    for searchRow in searchRows:
        search = {
            "uid": searchRow['uid'],
            "search": searchRow['search'],
            "timestamp": searchRow['timestamp'],
            "prediction_weight": searchRow['prediction_weight'],
            "attrs": searchRow['attrs']
        }
        search_history.append(search)
    return search_history


def insert_search_history(uid, search, timestamp, prediction_weight, attrs):
    verify_searchtable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO search (uid, search, timestamp, prediction_weight, attrs) VALUES (?, ?, ?, ?, ?)', (uid, search, timestamp, prediction_weight, attrs))
    conn.commit()
    conn.close()


def probabilistic_sample_recommender(uid, n_samples=10):
    verify_searchtable()
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search WHERE uid = ?', (uid,))
    searchRows = cursor.fetchall()
    conn.close()

    # Sum over all weights in searchRows.
    sum_weights = sum(float(searchRow['prediction_weight']) for searchRow in searchRows)
    if sum_weights == 0:
        return None
    
    # Normalize weights.
    normalised_weights = [searchRow['prediction_weight'] / sum_weights for searchRow in searchRows]
    
    search_samples = []
    for i in range(n_samples):
        # Sample a search result at random based on the corresponding weights.
        sample = random.random()
        cumulative = 0.0
        for searchRow, weight in zip(searchRows, normalised_weights):
            cumulative += weight
            if sample <= cumulative:
                search_samples.append((searchRow['search'], searchRow['attrs']))
                break

    return search_samples
