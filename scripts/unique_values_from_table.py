import sqlite3
#words_learnedword
# подключение к базе (замени на свой путь или параметры подключения)
conn = sqlite3.connect("../words.db")
cursor = conn.cursor()

# запрос уникальных значений
cursor.execute("SELECT DISTINCT part_of_speech FROM words;")

# получение всех строк
parts = cursor.fetchall()

# вывод
print("Уникальные значения part_of_speech:")
for row in parts:
    print(row[0])

# закрытие соединения
conn.close()
