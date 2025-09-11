import sqlite3

# Путь к твоей базе (замени на свой)
db_path = "../words2.db"

# Подключаемся
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Выводим
print("Список таблиц:")
for t in tables:
    print(t[0])

conn.close()


conn = sqlite3.connect('../words2.db')
cur = conn.cursor()

cur.execute("PRAGMA table_info(vocab)")
columns = cur.fetchall()

print("Columns in 'words':")
for col in columns:
    print(col[1])  # название колонки вторая позиция

cur.close()
conn.close()
