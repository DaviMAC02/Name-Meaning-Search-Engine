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
cursor_pages.execute("SELECT url FROM Pages where filtered is NULL and html is NULL")
links = cursor_pages.fetchall()

if not links:
    url = 'https://www.dicionariodenomesproprios.com.br/'
    html = urlopen(url, context=ctx).read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

    # Retrieve all of the anchor tags
    tags = soup('a')
    for tag in tags:
        # Look at the parts of a tag
        url = 'https://www.dicionariodenomesproprios.com.br' + tag.get('href', None)
        cursor_pages.execute("INSERT  OR IGNORE INTO Pages (url) VALUES (?)", (url,))
        conn_pages.commit()

i = int(input('How many pages do you want to retrieve?\n'))

for i in range(0,i):
        cursor_pages.execute("SELECT url FROM Pages where filtered is NULL and html is NULL")
        links = cursor_pages.fetchall()
        url =  links[0][0]  
        try:      
            html = urlopen(url, context=ctx).read()
        except:
            cursor_pages.execute("UPDATE Pages SET html = 'none' where url = ?", (url,))
            continue

        html = html.decode('utf-8')
        print('Retrieving: ' + url)
        cursor_pages.execute("UPDATE Pages SET html = ? where url = ?", (html,url))
        conn_pages.commit()
        soup = BeautifulSoup(html, "html.parser")
        

        # Retrieve all of the anchor tags
        tags = soup('a')
        for tag in tags:
            # Look at the parts of a tag
            url = 'https://www.dicionariodenomesproprios.com.br' + tag.get('href', None)
            cursor_pages.execute("INSERT  OR IGNORE INTO Pages (url) VALUES (?)", (url,))
            conn_pages.commit()



    