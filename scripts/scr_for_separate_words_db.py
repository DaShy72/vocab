import sqlite3
import wordninja
import re

def fix_text(text):
    if not text:
        return text

    # Разбиваем текст на слова и знаки препинания, оставляя апострофы внутри слов
    tokens = re.findall(r"\b[\w']+\b|[^\w\s]", text, re.UNICODE)

    result = ""
    for i, token in enumerate(tokens):
        result += token
        if i + 1 < len(tokens):
            next_token = tokens[i + 1]

            # Если текущий токен — слово и следующий — ' или 're'/'ve'/etc., объединяем
            if re.match(r"[\w]+", token) and next_token in ["' re", "' ve", "' ll", "' d", "' m", "' s", "' t"]:
                result += ""
            # Иначе добавляем пробел, если следующий токен — не знак препинания
            elif not re.match(r"[^\w\s]", next_token):
                result += " "

    return result





def merge_apostrophes(text):
    if not text:
        return text

    # Убираем пробел перед апострофом
    text = re.sub(r"\s+'", "'", text)
    # Убираем пробел после апострофа
    text = re.sub(r"'\s+", "'", text)

    return text




conn = sqlite3.connect('../words2.db')
cur = conn.cursor()

cur.execute("SELECT id, definition_examples FROM words")
rows = cur.fetchall()

for word_id, text in rows:
    fixed = merge_apostrophes(text)
    if fixed != text:
        cur.execute(
            "UPDATE words SET definition_examples = ? WHERE id = ?",
            (fixed, word_id)
        )

conn.commit()
cur.close()
conn.close()

print("All done!")
