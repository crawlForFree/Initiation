from bs4 import BeautifulSoup
import urllib.request
import re
from queue import Queue

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
def refine(link):
    a = "http"
    b = "https"
    if a in link or b in link:
        return True
    return False

print("Enter Seed Url : ")
seed_url = input()
print("Enter domain : ")
domain = input()
curr_links = set()
f = open("crawled.txt", "w+")

# trying to apply BFS algorithms to crawl

q = Queue()
q.put(seed_url)
while q.empty() is False:
    element_link=q.get_nowait()
    html_page = requests.get(element_link)
    data = html_page.text
    soup = BeautifulSoup(data, "html.parser")
    links = set()
    for link in soup.findAll('a'):
        temp = link.get('href',None)
        if temp is not None and domain in temp and refine(temp):
            links.add(temp)
    for i in links :
        if not i in curr_links:
            f.write(i)
            f.write("\n")
            print(i)
            curr_links.add(i)
            q.put(i)
f.close()
