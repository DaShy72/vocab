import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re

# файл со словами (по одному в строке)
WORDS_FILE = "txt_files/words_test.txt"
DB_FILE = "../words2.db"

# --- СОЗДАЕМ SQLite БАЗУ ---
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS dict (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    transcription TEXT,
    pos TEXT,
    translation TEXT
)
""")
conn.commit()

def parse_entry(text: str):
    # 1. убираем заголовок (до первой кириллической буквы)
    match = re.search(r"[А-Яа-яІЇЄҐіїєґ1]", text)
    if not match:
        return None
    content = text[match.start():].strip()

    # 2. ищем все блоки, начинающиеся с цифры
    # если цифра в начале блока (например "1. переводы ..."), ставим перед ней ||
    def insert_block_separator(match):
        return " || " + match.group(0)

    # добавляем "||" перед каждой цифрой, которая идёт в начале блока
    content = re.sub(r"(?<!\| )\b\d+\.", insert_block_separator, content)

    # 3. разделяем примеры с "to ~"
    parts = re.split(r"(?=to\s*~)", content)
    result_blocks = []
    for part in parts:
        block = part.strip().rstrip(";.")
        if block:
            result_blocks.append(block)

    # 4. объединяем всё через " | "
    result = " | ".join(result_blocks)
    return result


# читаем список слов
with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words = [w.strip() for w in f if w.strip()]

for w in words:
    url = f"https://e2u.org.ua/s?w={w}&dicts=17&main_only=on"
    print(f"[+] Fetching {url}")

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке {w}: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")

    # Все блоки со словарными статьями
    tds = soup.find_all("td", class_="result_row_main")
    for td in tds:
        b_tag = td.find("b")
        word = b_tag.get_text(strip=True) if b_tag else w

        span_tag = td.find("span", class_="IPA")
        transcription = span_tag.get_text(strip=True) if span_tag else ''

        # часть речи
        i_tag = td.find("i")
        pos = i_tag.get_text(strip=True) if i_tag else ""

        pos_map = {
            'adv': 'adverb',
            'v': 'verb',
            'n': 'noun',
            'a': 'adjective',
            'prep': 'preposition',
            'conj': 'conjunction',
            'pron': 'pronoun',
        }
        pos = pos_map.get(pos, pos)

        translation = str(td)
        if "</i>" in translation:
            translation = translation.split("</i>", 1)[1]

        if translation.endswith("</td>"):
            translation = translation[:-5]


        cur.execute(
            "INSERT INTO dict (word, transcription, pos, translation) VALUES (?, ?, ?, ?)",
            (word, transcription, pos, translation)
        )
        conn.commit()
        print(f"   -> {word}| {transcription} | {pos} | {translation}")
        time.sleep(0.3)




conn.close()

