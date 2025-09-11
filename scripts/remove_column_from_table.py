import sqlite3

def remove_column(db_path, table_name, column_to_remove):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем список колонок таблицы
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    if column_to_remove not in column_names:
        print(f"Колонка {column_to_remove} не найдена в таблице {table_name}")
        return

    # Формируем список колонок, которые останутся
    remaining_columns = [col for col in column_names if col != column_to_remove]
    columns_str = ", ".join(remaining_columns)

    # Формируем временное имя таблицы
    temp_table = table_name + "_temp"

    # Создаем новую таблицу с нужными колонками
    # Для этого получим схему таблицы и изменим ее
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    create_sql = cursor.fetchone()[0]

    # Изменяем схему: удаляем колонку из CREATE TABLE
    # Примерный способ: удалить из CREATE TABLE часть с колонкой
    # Лучше сделать более надежно, но для простых случаев достаточно

    def remove_column_from_create_sql(create_sql, col_name):
        start = create_sql.index('(')
        end = create_sql.rindex(')')
        cols_def = create_sql[start+1:end].split(',')
        cols_def = [c.strip() for c in cols_def]
        cols_def = [c for c in cols_def if not c.startswith(col_name + " ")]
        new_cols_def = ", ".join(cols_def)
        return create_sql[:start+1] + new_cols_def + create_sql[end:]

    new_create_sql = remove_column_from_create_sql(create_sql, column_to_remove)
    new_create_sql = new_create_sql.replace(table_name, temp_table)

    cursor.execute(new_create_sql)

    # Копируем данные в новую таблицу
    cursor.execute(f"INSERT INTO {temp_table} ({columns_str}) SELECT {columns_str} FROM {table_name}")

    # Удаляем старую таблицу
    cursor.execute(f"DROP TABLE {table_name}")

    # Переименовываем новую таблицу
    cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")

    conn.commit()
    conn.close()
    print(f"Колонка {column_to_remove} удалена из таблицы {table_name}")

# Пример вызова
remove_column("../words.db", "words", "translation")
