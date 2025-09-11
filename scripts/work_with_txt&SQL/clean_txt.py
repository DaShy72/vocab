# пути к файлам
file1_path = "words.txt"
file2_path = "../txt_files/words2.txt"
output_path = "../txt_files/unique_words.txt"

# читаем слова из первого файла
with open(file1_path, "r", encoding="utf-8") as f1:
    words1 = {line.strip() for line in f1 if line.strip()}

# читаем слова из второго файла
with open(file2_path, "r", encoding="utf-8") as f2:
    words2 = {line.strip() for line in f2 if line.strip()}

# находим уникальные слова
unique_words = (words1 - words2) | (words2 - words1)

# записываем результат в файл
with open(output_path, "w", encoding="utf-8") as out:
    for word in sorted(unique_words):
        out.write(word + "\n")

print(f"Готово! Уникальные слова сохранены в {output_path}")