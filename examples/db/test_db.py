import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS user_info
        (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

c.execute("INSERT INTO user_info (id, name, age) VALUES (1, 'Alice', 25)")
c.execute("SELECT * FROM user_info WHERE id=1")
print(f"Alice: {c.fetchall()}") # actually print the select statement
conn.commit()   # commit the changes made by the cursor c

# c.execute('''DROP TABLE IF EXISTS user_info''')  # Drop the table if it exists
# c.execute('''CREATE TABLE IF NOT EXISTS user_info
#         (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# c.execute("INSERT INTO user_info (name, age) VALUES ('Alice', 25)")
# c.execute("INSERT INTO user_info (name, age) VALUES ('Bob', 30)")
# conn.commit()   # commit the changes made by the cursor c

# # SELECT statement
# c.execute("SELECT * FROM user_info")
# print(f"All items: {c.fetchall()}")
# c.execute("SELECT * FROM user_info WHERE name='Alice'")
# print(f"Alice: {c.fetchall()}")
# c.execute("SELECT * FROM user_info WHERE age=25")
# print(f"Age 25: {c.fetchall()}")
# c.execute("SELECT * FROM user_info WHERE age > 25")
# print(f"Age > 25: {c.fetchall()}")
# c.execute("SELECT * FROM user_info WHERE age < 30")
# print(f"Age < 30: {c.fetchall()}")
# c.execute("SELECT * FROM user_info WHERE age BETWEEN 25 AND 30")
# print(f"Age 25-30: {c.fetchall()}")
# # ... etc.

# # Get an item with a particular key
# c.execute('SELECT * FROM user_info WHERE id=?', (1,))
# print(f"Item with id=1: {c.fetchone()}")

# # Modify an attribute of a particular element
# c.execute('UPDATE user_info SET age=? WHERE id=?', (20, 1))

# conn.commit()  # commit the changes made by the cursor c

# # Close the database connection
# conn.close()