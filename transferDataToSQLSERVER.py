import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import mysql.connector as mc
connection = mc.connect (host = "localhost",
                         user = "root",
                         passwd = "134113",
                         db = "db")
cursor = connection.cursor()
cursor.execute ("truncate table FORMS")
#cursor.execute("use db")

# file to fetch data from

# FOR TESTING PURPOSES
f = open("crawled.txt",'r')

#f = open(sys.argv[1], 'r')
forums = set()
login = set()
signup = set()
search_forms = set()


login_list = ['login', "LOGIN", "LOG IN", "Sign In", "SIGN IN", "SIGNIN", 'Log In']
signup_list = ['Already have an account','REGISTER','register','signup', "SIGN UP", 'SIGNUP', 'Sign Up', 'SignUp' , 'Create Account','create account', 'CREATE ACCOUNT','createaccount' ]
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


def fetchComponents(link, string):
    filterIn = {'hidden','text','selectors'}
    typo = []
    kmpSearch('type=',string,0,len(string),typo)
    for i in typo:
        x= i
        while string[x] is not '>':
            x = x + 1
        limo = FETCHER(string[i:x], 'type=')
        ok = 1
        for j in filterIn:
            if j in limo:
                ok=0
                break
        if ok is 1:
            link += ", " + limo

    return link

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
    # print(link)
    if Ftype is 'LOGIN':
        link = fetchComponents(link ,string[start:end+1])
        login.add(link)
        x = link.split(',')
        print(x)
        TYPE = "LOGIN"
        URL = x[0]
        ID = x[1]
        METHOD = x[2]
        ACTION = x[3]
        i = 4
        INFO = str()
        print(len(x))
        while i < len(x):    
            INFO = INFO + " " + x[i]
            i+=1
        format_str = """INSERT INTO FORMS (TYPE, URL, ID, METHOD, ACTION,ADDITIONAL_INFO) 
                        VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}');"""
        command = format_str.format(a = TYPE, b = URL, c = ID, d = METHOD, e = ACTION, f = INFO)
        cursor.execute(command) 
        connection.commit()  
    if Ftype is 'SIGNUP':
        signup.add(link)
        x = link.split(',')
        print(x)
        TYPE = "SIGNUP"
        URL = x[0]
        ID = x[1]
        METHOD = x[2]
        ACTION = x[3]
        i = 4
        INFO = str()
        print(len(x))
        while i < len(x):    
            INFO = INFO + " " + x[i]
            i+=1
        format_str = """INSERT INTO FORMS (TYPE, URL, ID, METHOD, ACTION,ADDITIONAL_INFO) 
                        VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}');"""
        command = format_str.format(a = TYPE, b = URL, c = ID, d = METHOD, e = ACTION, f = INFO)
        cursor.execute(command) 
        connection.commit()  
    if Ftype is 'SEARCH':
        search_forms.add(link)
        x = link.split(',')
        TYPE = "SEARCH"
        URL = x[0]
        ID = x[1]
        METHOD = x[2]
        ACTION = x[3]
        i = 4
        INFO = str()
        print(len(x))
        while i < len(x):    
            INFO = INFO + " " + x[i]
            i+=1
        format_str = """INSERT INTO FORMS (TYPE, URL, ID, METHOD, ACTION,ADDITIONAL_INFO) 
                        VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}');"""
        command = format_str.format(a = TYPE, b = URL, c = ID, d = METHOD, e = ACTION, f = INFO)
        cursor.execute(command) 
        connection.commit()  


def ClassifyIt(link, string, start, end):
    # 1.LOGIN
    for i in login_list:
        if re.search(i, string[start:end + 1], re.MULTILINE | re.I) is not None:
            IdentifyStuff(link, string, start, end, 'LOGIN')
            break
    # 2.SIGNUP
    for i in signup_list:
        if re.search(i, string[start:end + 1], re.MULTILINE | re.I) is not None:
            IdentifyStuff(link, string, start, end, 'SIGNUP')
            break
    # 3.SEARCH
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
cursor.close()
connection.close()
