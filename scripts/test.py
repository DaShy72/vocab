import random
import time
import test2
import requests
import sqlite3
from bs4 import BeautifulSoup

BASE_URL = "https://www.oxfordlearnersdictionaries.com{}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


with open('txt_files/links_text.txt', "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

for word in words:
    url = BASE_URL.format(word)
    try:
        time.sleep(random.randint(4,7))
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
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

        result_text = "/".join(result_lines)


        formatted_words = [test2.split_mixed_case_word(w) for w in result_text.split()]
        #formatted_text = " ".join(formatted_words)

        with open("definitions_examples.txt", "w", encoding="utf-8") as f:
            f.write(formatted_words)
        print(formatted_words)

        print("Готово! Результат сохранён в definitions_examples.txt")
    except Exception as e:
        print(f"[ERROR] {word}: {e}")



