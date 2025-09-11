import sqlite3

conn = sqlite3.connect("words2.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM dict ")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()