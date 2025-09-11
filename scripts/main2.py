import requests
from bs4 import BeautifulSoup

url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
response.raise_for_status()


soup = BeautifulSoup(response.text, "html.parser")


with open("txt_files/links.txt", "w", encoding="utf-8") as file:
    for li in soup.find_all("li"):
        # слово
        a_tag = li.find("a")
        link = a_tag["href"] if a_tag and "href" in a_tag.attrs else ""

        # записываем строку в файл
        file.write(f"{link}\n")

print("Готово! Данные сохранены в parsed_words.txt")
