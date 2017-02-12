import requests as re
from bs4 import BeautifulSoup
import urllib.request

# file to fetch data from

f = open("crawled.txt", 'r')
forums = set()
login = set()
submit = set()
signup = set()
forgot_pass = set()
search_forms = set()


login_list = ['login', "LOGIN", "LOG IN", "Sign In", "SIGN IN", "SIGNIN", 'Log In']
signup_list = ['Already have an account','REGISTER','register','signup', "SIGN UP", 'SIGNUP', 'Sign Up', 'SignUp' , 'Create Account','create account', 'CREATE ACCOUNT','createaccount' ]
forgot_passwd = ['recover','Forgotten','Forgot','forgot','forgotten']
search_keys = ['search','SEARCH','Search']


def controlledId(expression, key):
    try:
        pos = expression.find(key)
    except:
        return None
    if pos == -1:
        return None
    pos += len(key)
    while expression[pos] == ' ':
        pos += 1
    pos += 1
    while expression[pos] == ' ':
        pos += 1
    id = ""
    while pos < len(expression):
        id += expression[pos]
        pos += 1
        if expression[pos] is '"' or expression[pos] is "'":
            break
    return id

def getloginid(html_data, searchListing):
    startt = html_data.find('<form')
    endd = html_data.find('</form>')
    while True:
        if startt is -1:
            break
        temp = html_data[startt : endd + 7]
        for worm in searchListing:
            if worm in temp:
                try:
                    x=temp.find(worm)
                    id =controlledId(temp,' id=')
                    id += ','+controlledId(temp,' method=')
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
    link=link.split('\n')
    link=link[0]
    try:
        html_page = re.get(link)
        data = html_page.text
        soup = BeautifulSoup(data, "html.parser")
        getTemplate = soup.prettify()
        upform = getTemplate.upper()
        if '</form>' in getTemplate and link not in forums:
            # looking for a search page like google search page , yahoo , youtube etc . . ..
            forums.add(link)
            for worm in search_keys:
                if worm in getTemplate:
                    if link not in search_forms:
                        id = getloginid(getTemplate, search_keys)
                        if id is None:
                            continue
                        print(id)
                        search_forms.add(link + ',' + id)
                    break
            # check if its a signup form
            for worm in signup_list:
                if worm in getTemplate:
                    if link not in signup:
                        id = getloginid(getTemplate, signup_list)
                        if id is None:
                            continue
                        print(id)
                        signup.add(link + ',' + id)
                    break
             # check if its a login page!!
            if 'LOGIN' in upform or 'LOG IN' in upform or 'SIGNIN' in upform or 'SIGN IN' in upform:
                if link not in login:
                    id = getloginid(getTemplate, login_list)
                    if id is None:
                        continue
                    print(id)
                    login.add(link + ',' + id)
            # check if it is a forgot password form
            for worm in forgot_passwd:
                if worm in getTemplate:
                    if link not in forgot_pass:
                        id = getloginid(getTemplate, forgot_passwd)
                        if id is None:
                            continue
                        print(id)
                        forgot_pass.add(link + ',' + id)
                    break



    except:
        pass



f.close();
f=open("forms_detected.txt", 'w+')
for link in forums:
    f.write(link+"\n")
f.close()

# Making a file containing login, signup ,search forms
# Appearance :
#       URL  |   ID  |  METHOD
f = open("login_forms.csv","w+")
f.write("URL,ID,METHOD\n")
for links in login:
    f.write(links+"\n")
f.close()

f = open("signup_forms.csv","w+")
f.write("URL,ID,METHOD\n")
for links in signup:
    f.write(links+"\n")
f.close()

f = open("search.csv","w+")
f.write("URL,ID,METHOD\n")
for links in search_forms:
    f.write(links+"\n")
f.close()
