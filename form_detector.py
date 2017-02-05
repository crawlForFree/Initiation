import requests as re
from bs4 import BeautifulSoup
import urllib.request

f = open("crawlled.txt", 'r')
forums = set()
login = set()
submit = set()

login_list = ["login" , "LOGIN" , "LOG IN" , "Sign In", "SIGN IN" , "SIGNIN", 'Log In']


def getloginid(html_data):
    startt = html_data.find('<form')
    endd = html_data.find('</form>')
    while True:
        if startt is -1:
            break
        temp = html_data[startt : endd + 7]
        for worm in login_list:
            if worm in temp:
                try:
                    x = temp.find(worm)
                    pos  = temp.find(' id')+3
                    while temp[pos] == ' ':
                        pos+=1
                    pos+=1
                    while temp[pos] == ' ':
                        pos += 1
                    pos+=1
                    id = ""
                    while pos < len(temp):
                        id += temp[pos]
                        pos+=1
                        if temp[pos] is '"' or temp[pos] is "'":
                            break
                    return id

                except:
                    pass
        matter=html_data[endd :]
        adder = matter.find('<form ')
        if adder is -1:
            break
        startt = endd + adder
        matter=html_data[endd+7 :]
        endd = endd + 7 + matter.find('</form>')




for link in f:
    try:
        html_page = re.get(link)
        data = html_page.text
        soup = BeautifulSoup(data, "html.parser")
        getTemplate = soup.prettify()
        upform = getTemplate.upper()
        if '</form>' in getTemplate and link not in forums:
            forums.add(link)
            # check if its a login page!!
            if 'LOGIN' in upform or 'LOG IN' in upform or 'SIGNIN' in upform or 'SIGN IN' in upform:
                if link not in login:
                    id = getloginid(getTemplate)
                    if id is None:
                        continue
                    login.add(link+id)
            # check if its a submission or online transactions form or submit comment
            elif 'SUBMIT' in upform:
                submit.add(link)

    except:
        pass

f.close();
f=open("forms_detected.txt", 'w+')
for link in forums:
    f.write(link)
f.close()

# Making a file containing login forms
# Appearance :
#       Line one will contain URL containing login form
#       Line two will contain the HTML id of login form
f = open("login_forms.txt","w+")
for links in login:
    f.write(links+"\n")
f.close()
