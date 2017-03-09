import requests
from bs4 import BeautifulSoup
import urllib.request
import re

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


def kmpSearch(pattern, string, start_index, ending_index, arr = []):
    m = len(pattern)
    LPSarray = []
    computeLPS(pattern,m,LPSarray)
    i = start_index
    j = 0
    n = ending_index
    while i < n:
        if (pattern[j] is string[i]):
            i+=1
            j+=1
        if j is m:
            arr.append(i-j)
            j = LPSarray[j-1]
        else:
            if i < n and pattern[j] is not string[i]:
                if j is not  0:
                    j = LPSarray[j-1]
                else :
                    i+=1



def computeLPS(pattern, m, LPS = []):
    length = 0
    for i in range(0,m):
        LPS.append(0)
    i = 1
    while i < m:
        if pattern[i] is pattern[length]:
            length+=1
            LPS[i] = length
            i+=1
        else:
            if length is not 0:
                length = LPS[length-1]
            else:
                LPS[i] = 0
                i+=1

def FETCHER(expression, key):
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

def fetchDomain(s):
    com = s.find('com')
    return s[0:com+3]

def fancy_action(ac):
    final_index = 0
    for i in range(0,len(ac)):
        if ac[i] is ';':
            final_index = i
            break

    return ac[0:final_index]

def IdentifyStuff(link, string , start, end, Ftype):
    save_link = link
    # FETCH ID
    id = FETCHER(string[start:end+1],'id=')
    if id is None:
        link += ',  NOT_PRESENT'
    else :
        link += ',  ' + id

    # FETCH METHOD
    method = FETCHER(string[start:end + 1], 'method=')
    if method is None:
        link += ',  NOT_PRESENT'
    else:
        link += ',  ' + method

    # FETCH ACTION
    action = FETCHER(string[start:end + 1], 'action=')
    action = fancy_action(action)
    if action is None:
        link += ',  NOT_PRESENT'
    else:
        link += ( ',  ' )
        if 'http' not in method:
            link += str(fetchDomain(save_link))
        link += action
    print(link)
    if Ftype is 'LOGIN':
        login.add(link)
    if Ftype is 'SIGNUP':
        signup.add(link)
    if Ftype is 'SEARCH':
        search_forms.add(link)


def ClassifyIt(link, string, start, end):
    condition1 = False
    condition2 = False
    # print(condition1, condition2)
    #1.SIGNUP
    for i in signup_list:
        if re.search(i, string[start:end + 1], re.MULTILINE | re.I) is not None:
            IdentifyStuff(link, string, start, end, 'SIGNUP')
            condition1 = True
            break
    # print(condition1, condition2)
    #2.LOGIN
    if condition1 is False:
        for i in login_list:
            if re.search(i, string[start:end + 1], re.MULTILINE | re.I) is not None:
                IdentifyStuff(link, string, start, end, 'LOGIN')
                condition2 = True
                break
    # print(condition1, condition2)
    # 3.SEARCH
    if condition1 is False and condition2 is False:
        for i in search_keys:
            if re.search(i,string[start:end+1],re.MULTILINE | re.I) is not None:
                IdentifyStuff(link, string , start, end, 'SEARCH')
                break


def DivideIt(link,string):
    start_index = []
    end_index = []
    kmpSearch('<form',string,0,len(string),start_index)
    kmpSearch('</form>',string,0,len(string),end_index)
    #****************UNCOMMENT TO PRINT START AND ENDING INDICES OF RESPECTIVE FORMS*********************
    # for i in start_index:
    #     print(i,end=' ')
    # print("")
    # for i in end_index:
    #     print(i,end=' ')
    #****************************************************************************************************
    j=0
    for i in range(0,len(start_index)):
       while j < len(end_index) and end_index[j] < start_index[i]:
           j+=1
       # FROM COUNT STARTS HERE
       ClassifyIt(link,string,start_index[i],end_index[j])

for link in f:
    link=link.split('\n')
    link=link[0]
    try:
        html_page = requests.get(link)
        data = html_page.text
        soup = BeautifulSoup(data, "html.parser")
        #print(soup)
        template = soup.prettify()
        if '</form>' in template and link not in forums:
            forums.add(link)
            DivideIt(link,template)
    except:
        pass


f.close()
f=open("forms_detected.txt", 'w+')
for link in forums:
    f.write(link+"\n")
f.close()

# Making a file containing login, signup forms
# Appearance :
#       URL  |   ID  |  METHOD
f = open("login_forms.csv","w+")
f.write("URL,ID,METHOD,ACTION\n")
for links in login:
    f.write(links+"\n")
f.close()

f = open("signup_forms.csv","w+")
f.write("URL,ID,METHOD,ACTION\n")
for links in signup:
    f.write(links+"\n")
f.close()

f = open("search.csv","w+")
f.write("URL,ID,METHOD,ACTION\n")
for links in search_forms:
    f.write(links+"\n")
f.close()


