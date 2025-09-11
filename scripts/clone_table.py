import sqlite3

# исходная база
src_conn = sqlite3.connect("../dictionary.db")
src_cur = src_conn.cursor()

# целевая база
dst_conn = sqlite3.connect("../words2.db")
dst_cur = dst_conn.cursor()

# 1. получаем схему таблицы
table_name = "dict"
src_cur.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
create_table_sql = src_cur.fetchone()[0]

# 2. создаём таблицу в новой базе
dst_cur.execute(create_table_sql)

# 3. копируем все данные
src_cur.execute(f"SELECT * FROM {table_name}")
rows = src_cur.fetchall()
dst_cur.executemany(f"INSERT INTO {table_name} VALUES ({','.join(['?']*len(rows[0]))})", rows)

# сохраняем изменения
dst_conn.commit()

# закрываем соединения
src_conn.close()
dst_conn.close()

print("Таблица успешно скопирована!")
