"""
FTPScan by StYl3z
Greetz fly out to:
L0rd,Legolas,Prometheus,Smoky-Ice,izibitzi,Waterb0ng,MaXtOr
usage: python3 ftpscan.py <startip> <endip>
"""
import re
import socket
import sys
import threading

def Check(ip,port):    
    try:
        s = socket.socket()
        s.settimeout(0.3)
        s.connect((ip,port))
        s.send("\r\n")
        print(s.recvmsg(4096))
        if "FTP" in s.recvmsg(4096).decode('utf-8'):
            retard = open('ftps.txt','a')
            retard.write(ip+"\n")
            retard.close()
    except:
        return    

def Scan():
    start = sys.argv[1]
    end = sys.argv[2]    
    endip = end.split('.')
    currentip = start.split('.')
    while not (currentip == endip):
        targetip = currentip[0]+"."+currentip[1]+"."+currentip[2]+"."+currentip[3]
        print("Checking: "+targetip+"\n")
        thread = threading.Thread(target=Check,args=(targetip,21))
        if threading.activeCount()<500:        
            thread.start()
        else:
            thread.join()        
        if not (int(currentip[3])==255):
            currentip[3] = int(currentip[3])+1
            currentip[3] = str(currentip[3])
        else:
            if not(int(currentip[2])==255):
                currentip[2] = int(currentip[2])+1
                currentip[2] = str(currentip[2])
                currentip[3] = str("0")
            else:
                if not(int(currentip[1])==255):
                    currentip[1] = int(currentip[1])+1
                    currentip[1] = str(currentip[1])
                    currentip[2] = str("0")
                    currentip[3] = str("0")                    
                else:
                    if not(int(currentip[0])==255):
                        currentip[0] = int(currentip[0])+1
                        currentip[0] = str(currentip[0])
                        currentip[1] = str("0")
                        currentip[2] = str("0")
                        currentip[3] = str("0")
                
Scan()