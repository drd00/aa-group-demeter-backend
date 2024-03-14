import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS user_info''')  # Drop the table if it exists

conn.commit()   # commit the changes made by the cursor c