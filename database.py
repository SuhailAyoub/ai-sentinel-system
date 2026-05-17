import sqlite3

connection = sqlite3.connect("ai_dashboard.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS monitoring (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT,
    toxicity INTEGER,
    score INTEGER,
    alert TEXT
)
""")

connection.commit()

connection.close()

print("Database Created Successfully")