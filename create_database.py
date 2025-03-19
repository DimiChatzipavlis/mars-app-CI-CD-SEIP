import sqlite3

conn = sqlite3.connect('mars_resources.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()