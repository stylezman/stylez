"""
PortScanner v0.01
"""
import socket
import threading
import sys
import time
def CheckIfOpen(ip,port):
    target = (ip,int(port))
    try:
        socket.create_connection(target,1.5)
        open('open','a').write(ip+":"+str(port)+"\n")
        print("Port: "+str(port)+" open on IP: "+ip+"!\n")
    except:
        print("Port: "+str(port)+" closed on IP: "+ip+"!\n")
if sys.argv[4]:
    threads = int(sys.argv[4])
else:
    threads = 100
start = sys.argv[1].split(".")
end = sys.argv[2].split(".")
if int(end[3]) != 255:
    end[3] = int(end[3])+1
else:
    if int(end[2]) != 255:
        end[2] = int(end[2])+1
        end[3] = 0
    else:
        if int(end[1]) != 255:
            end[1] = int(end[1])+1
            end[2] = 0
            end[3] = 0
        else:
            if int(end[0]) != 255:
                end[0] = int(end[0])+1
                end[1] = 0
                end[2] = 0
                end[3] = 0
end = str(end[0])+"."+str(end[1])+"."+str(end[2])+"."+str(end[3])
current = str(start[0])+"."+str(start[1])+"."+str(start[2])+"."+str(start[3])
try:
    ports = sys.argv[3].split(",")
except:
    ports = sys.argv[3]
while(current != end):
    for port in ports:
        if threading.active_count() <= int(threads):
            T = threading.Thread(target=CheckIfOpen,args=(current,int(port),))
            T.start()
        else:
            time.sleep(0.2)
            T = threading.Thread(target=CheckIfOpen,args=(current,int(port),))
            T.start()
    progress = current.split(".")
    if int(progress[3]) != 255:
        progress[3] = int(progress[3])+1
    else:
        if int(progress[2]) != 255:
            progress[2] = int(progress[2])+1
            progress[3] = 0
        else:
            if int(end[1]) != 255:
                progress[1] = int(progress[1])+1
                progress[2] = 0
                progress[3] = 0
            else:
                if int(progress[0]) != 255:
                    progress[0] = int(progress[0])+1
                    progress[1] = 0
                    progress[2] = 0
                    progress[3] = 0
    current = str(progress[0])+"."+str(progress[1])+"."+str(progress[2])+"."+str(progress[3])
T.join()
print("Scan finished!\n")
exit()