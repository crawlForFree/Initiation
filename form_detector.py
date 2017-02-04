import requests as re
from bs4 import BeautifulSoup
import urllib.request

f = open("crawled.txt", 'r')
forums = set()

for link in f:
    try:
        html_page = re.get(link)
        data = html_page.text
        soup = BeautifulSoup(data, "html.parser")
        if '<form' in soup.prettify() and link not in forums:
            forums.add(link)
    except:
        pass

f.close();
f=open("forms_detected.txt", 'w+')
for link in forums:
    f.write(link)
f.close()
