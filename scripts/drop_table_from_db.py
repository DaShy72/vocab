import sqlite3

conn = sqlite3.connect('../words2.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS dict")

conn.commit()
conn.close()

"""
words
sqlite_sequence

words_vocab
words_dict











"""