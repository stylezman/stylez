"""
Portscanner for FXP-Terminal
Python 3.8.4
Coded by StYl3z
respect all Crews
"""
import ipaddress
import socket
import threading
Subnet = ""
Ports = ["21","80","445","1433","3306","3389","8080"]
Threads = []

def ScanPort(target,port):
    try:
        s=socket.socket()
        s.settimeout(0.9)
        s.connect((target,int(port)))
        s.send("\r\n")
        result = s.recv(512)
        if 'FTP' in result.decode('utf-8'):
            f = open('ftp','a')
            f.write(target+" "+result+"\n")
            f.close
        else:
            f = open('open','a')
            f.write(target+":"+port+"\n")
            f.close()
    except:
        pass
    finally:
        s.close()

IPs = ipaddress.ip_network(Subnet)
for Host in IPs.hosts():
    for Port in Ports:
        Threads.append(threading.Thread(target=ScanPort,args=(Host,Port)))
for Thread in Threads:
    if threading.active_count < 500:
        Thread.start()