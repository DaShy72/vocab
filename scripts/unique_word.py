import re

INPUT_FILE = "txt_files/words_unique.txt"

# читаем строки
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

cleaned_words = []
seen = set()

for line in lines:
    # убираем префикс "/definition/english/"
    word = line.replace("/definition/english/", "")
    # убираем суффикс _число или просто число
    word = re.sub(r'(_\d+|\d+)$', '', word)

    # добавляем только уникальные
    if word not in seen:
        seen.add(word)
        cleaned_words.append(word)

# перезаписываем файл
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    for w in cleaned_words:
        f.write(w + "\n")

print(f"Готово! Было {len(lines)} строк, осталось {len(cleaned_words)} уникальных слов.")
