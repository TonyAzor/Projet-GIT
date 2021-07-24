import socket, time, os
from datetime import datetime
from threading import Thread

path = "/tmp/Scan/"  
portDict = dict()

def scan(firstPort, lastPort):
    global portDict
    target = socket.gethostbyname(socket.gethostname())
    try:
        for port in range(firstPort,lastPort):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            # returns an error indicator
            result = s.connect_ex((target,port))
            if result ==0:
                portDict[str(port)]= "\nPort {} is open".format(port)
            else:
                portDict[str(port)]= "\nPort {} is closed".format(port)
            s.close()
          
    except KeyboardInterrupt:
            portDict["e"] = "\n Exitting Program !!!!"
    except socket.gaierror:
            portDict["e"] = "\n Hostname Could Not Be Resolved !!!!"
    except socket.error:
           portDict["e"] = "\\ Server not responding !!!!"

def addDict(port,line):
    portDict[port] = line

def printResult(firstPort, lastPort):
    target = socket.gethostbyname(socket.gethostname())
    global portDict 
    portDict = dict()
    x = (lastPort-firstPort)//3

    threadList = list()
    if x!=0:
        for mult in range(3):
            scanThread = Thread(target=scan, args=(firstPort+x*mult,firstPort+x*(mult+1)))
            scanThread.start()
            threadList.append(scanThread)
    scanThread = Thread(target=scan, args=(firstPort+x*3,lastPort+1))
    scanThread.start() 
    threadList.append(scanThread) 
    for thread in threadList:
        thread.join()

    
    with open(path+"portScanLogs.txt","w") as scanFile:  
        # Add Banner 
        scanFile.write("-" * 50+'\n')
        scanFile.write("Scanning Target: " + target+'\n')
        scanFile.write("Scanning started at:" + str(datetime.now())+'\n')
        scanFile.write("-" * 50+'\n')
        for port in range(firstPort,lastPort+1):
            scanFile.write(portDict[str(port)])
    
        

def start():
    while True:
        time.sleep(5)
        if os.path.exists(path+"portScanLogs.txt"):
            continue
        else:
            files = os.listdir(path)
            for File in files:
                if ".scan" in File:
                    ports = File[:-5].split("-")
                    if len(ports) == 1 and ports[0].isnumeric():
                        if int(ports[0]) > 0 and int(ports[0])<65536:
                            printResult(1,int(ports[0]))
                    elif len(ports) == 2 and ports[0].isnumeric() and ports[1].isnumeric():
                        if int(ports[0]) > 0 and int(ports[0])<=int(ports[1]) and int(ports[1])<65536:
                            printResult(int(ports[0]),int(ports[1]))
                os.unlink(path+File)     


start()