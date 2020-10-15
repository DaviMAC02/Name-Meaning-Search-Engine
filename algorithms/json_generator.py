import sqlite3

conn_pages = sqlite3.connect('pages.sqlite')
cursor_pages = conn_pages.cursor()

conn_filter = sqlite3.connect('filteredData.sqlite')
cursor_filter = conn_filter.cursor()

fhand = open('../js/name_meaning.json', 'w', encoding='utf-8')

fhand.write('{\n "meaning_pearson":[\n')

cursor_filter.execute("SELECT name, meaning FROM NameMeaning")

person_meaning = cursor_filter.fetchall()


for person in person_meaning:
    person = list(person)
    person[1] = person[1].replace('"', ' ')
    fhand.write('{"nome": "' + person[0].lower() + '", "meaning": "' + person[1] + '"},\n')
    cursor_filter.execute("UPDATE NameMeaning SET jsonADD = 'added' where name = ?", (person[0], ))
    conn_filter.commit()

fhand.write(']\n};')