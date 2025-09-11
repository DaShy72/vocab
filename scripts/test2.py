import re


def split_mixed_case_word(word):
    # Разделяем перед каждой заглавной буквой (но не в начале слова)
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', word)

# Обрабатываем каждое слово отдельно

