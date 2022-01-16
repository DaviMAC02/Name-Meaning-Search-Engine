from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import sqlite3

# Ignore SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn_pages = sqlite3.connect('pages.sqlite')

cursor_pages = conn_pages.cursor()
cursor_pages.execute("SELECT url FROM Pages where filtered is NULL and html is not NULL")
links = cursor_pages.fetchall()

i = input('How many pages do you want to retrieve?')

if not links:
    url = 'https://www.dicionariodenomesproprios.com.br/'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    cursor_pages.execute("INSERT  OR IGNORE INTO Pages (html) VALUES (?) where url = '?'", (html,url))
    conn_pages.commit()

    # Retrieve all of the anchor tags
    tags = soup('a')
    for tag in tags:
        # Look at the parts of a tag
        print('URL:', tag.get('href', None))
        cursor_pages.execute("INSERT  OR IGNORE INTO Pages (url) VALUES (?)", (tag.get('href', None)))
        conn_pages.commit()
else:
    for i in range(0,i):
        cursor_pages.execute("SELECT url FROM Pages where filtered is NULL and html is not NULL")
        links = cursor_pages.fetchall()


