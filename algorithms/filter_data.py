import sqlite3
from bs4 import BeautifulSoup
import re


conn_pages = sqlite3.connect('pages.sqlite')
cursor_pages = conn_pages.cursor()

conn_filter = sqlite3.connect('filteredData.sqlite')
cursor_filter = conn_filter.cursor()

cursor_filter.execute('''CREATE TABLE IF NOT EXISTS NameMeaning
    (id INTEGER PRIMARY KEY, name TEXT,
     meaning TEXT)''')

cursor_pages.execute("SELECT url FROM Pages where filtered is NULL and html is not NULL")

links = cursor_pages.fetchall()

for link in links:
    cursor_pages.execute("SELECT html FROM Pages where url = ?", (link[0], ))

    html = cursor_pages.fetchone()[0]

    soup_of_html = BeautifulSoup(html, "html.parser")

    meaning_tags = soup_of_html.select('div#significado')

    if not meaning_tags: 
        cursor_pages.execute("UPDATE Pages SET filtered = 'done' where url = ?", (link[0], ))
        conn_pages.commit()
        continue

    nome = soup_of_html.find("h1").text
    nome = nome.strip()
    nome = nome.replace('\n', '')

    result_meaning = re.findall('<strong>.+</strong>:\s+(.+i?</p>?)', str(meaning_tags[0]))

    result_meaning_pos = result_meaning[0].find(".")

    result_meaning[0] = result_meaning[0][:result_meaning_pos + 1]

    print("Inserting " + nome + " and its meaning...")

    cursor_filter.execute("INSERT OR IGNORE INTO NameMeaning (name, meaning) VALUES (?, ?)", (nome, result_meaning[0]))
    conn_filter.commit()

    cursor_pages.execute("UPDATE Pages SET filtered = 'done' where url = ?", (link[0], ))
    conn_pages.commit()












