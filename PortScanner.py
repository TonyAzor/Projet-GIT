import socket
from datetime import datetime
   

   
def scan(args):
    target = socket.gethostbyname(socket.gethostname()) 


    with open("PortScanLog.txt","w") as scanFile:  
        # Add Banner 
        scanFile.write("-" * 50+'\n')
        scanFile.write("Scanning Target: " + target+'\n')
        scanFile.write("Scanning started at:" + str(datetime.now())+'\n')
        scanFile.write("-" * 50+'\n')
    
        try:
            
            # will scan ports between 1 to 65,535
            for port in range(0,int(args)+1):
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