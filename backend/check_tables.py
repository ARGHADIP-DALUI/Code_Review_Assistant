import sqlite3

# This should match the path from app.db.session (usually same folder)
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("✅ Tables in the database:")
for table in tables:
    print("-", table[0])

conn.close()
