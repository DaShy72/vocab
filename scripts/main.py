import requests
import sqlite3
from bs4 import BeautifulSoup
import time
import random
import test2

# === Путь к файлу со словами ===
WORDS_FILE = "txt_files/links_text.txt"

# === Базовая ссылка (примерная) ===
BASE_URL = "https://www.oxfordlearnersdictionaries.com{}"


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

headers = {
    "User-Agent": random.choice(user_agents)
}



# === Создание SQLite базы и таблицы ===
conn = sqlite3.connect("words.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    part_of_speech TEXT,
    level TEXT,
    translation TEXT,
    transcription TEXT,
    definition_examples TEXT
)
""")
conn.commit()

# === Загрузка слов из файла ===
with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]
count = 0
time_work = 0
for word in words:
    url = BASE_URL.format(word)
    count += 1
    try:
        random_time = random.randint(4, 6)
        time_work = time_work + random_time
        time.sleep(random_time)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        word_text = soup.find('h1', class_='headword')
        word_text = word_text.get_text(strip=True) if word_text else ""

        # Часть речи
        part_of_speech = soup.find('span', class_='pos')
        part = part_of_speech.get_text(strip=True) if part_of_speech else ""

        # Уровень слова
        level = soup.find('div', class_='symbols')
        lvl = level.find("a")
        level_text = lvl["href"] if lvl and "href" in lvl.attrs else ""
        lvl_text = level_text[-2:]

        # Транскрипция
        phon = soup.find("span", class_="phon")
        transcription = phon.get_text(strip=True) if phon else ""
        transcription = transcription[:]

        #Определения и примеры
        result_lines = []
        for sense_li in soup.find_all("li", class_="sense"):
            # Определение
            def_tag = sense_li.find("span", class_="def")
            definition = def_tag.get_text(strip=True) if def_tag else ""

            # Примеры
            examples_list = []
            examples_ul = sense_li.find("ul", class_="examples")
            if examples_ul:
                for ex_li in examples_ul.find_all("li"):
                    examples_list.append(ex_li.get_text(strip=True))

            # Формируем строку: определение | пример1; пример2; ...
            examples_str = "; ".join(examples_list)
            line = f"{definition}|{examples_str}"
            result_lines.append(line)

        result_text = "||".join(result_lines)

        formatted_words = [test2.split_mixed_case_word(w) for w in result_text.split()]
        definition_examples_text = " ".join(formatted_words)



        cursor.execute("""
            INSERT INTO words (word, part_of_speech, level, translation, transcription, definition_examples)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (word_text, part, lvl_text, "", transcription, definition_examples_text))


        print(f"{count} [OK] {word}")


    except Exception as e:
        print(f"[ERROR] {word}: {e}")

conn.commit()
conn.close()
print(f"✅ Готово! Данные сохранены в words.db - time work - {time_work} sec")
