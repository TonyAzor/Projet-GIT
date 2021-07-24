import socket, time, os
from datetime import datetime

path = "/tmp/Scan/"  

   
def scan(firstPort, lastPort):
    target = socket.gethostbyname(socket.gethostname()) 

    
    with open(path+"portScanLogs","w") as scanFile:  
        # Add Banner 
        scanFile.write("-" * 50+'\n')
        scanFile.write("Scanning Target: " + target+'\n')
        scanFile.write("Scanning started at:" + str(datetime.now())+'\n')
        scanFile.write("-" * 50+'\n')
    
        try:
            
            # will scan ports between 1 to 65,535
            for port in range(firstPort,lastPort+1):
                if port == 0:
                    continue
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                
                # returns an error indicator
                result = s.connect_ex((target,port))
                if result ==0:
                    scanFile.write("\nPort {} is open".format(port))
                else:
                    scanFile.write("\nPort {} is closed".format(port))
                s.close()
                
        except KeyboardInterrupt:
                scanFile.write("\n Exitting Program !!!!")
        except socket.gaierror:
                scanFile.write("\n Hostname Could Not Be Resolved !!!!")
        except socket.error:
                scanFile.write("\\ Server not responding !!!!")

def start():
    while True:
        time.sleep(5)
        if os.path.exists(path+"portScanLogs"):
            continue
        else:
            files = os.listdir(path)
            for File in files:
                if ".scan" in File:
                    ports = File[:-5].split("-")
                    if len(ports) == 1 and ports[0].isnumeric():
                        if int(ports[0]) > 0 and int(ports[0])<65536:
                            scan(1,int(ports[0]))
                    elif len(ports) == 2 and ports[0].isnumeric() and ports[1].isnumeric():
                        if int(ports[0]) > 0 and int(ports[0])<=int(ports[1]) and int(ports[1])<65536:
                            scan(int(ports[0]),int(ports[1]))
                os.unlink(path+File)       

start()