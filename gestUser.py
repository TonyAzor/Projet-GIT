import json, os, pprint, getpass, paramiko,sys
import AS
from clear import clear


current_user = None


def authentication():
    clear()
    ID = input("Veuillez entrer votre ID : ")
    pwd = getpass.getpass("Veuillez entrer votre mot de passe : ")
    try:

        # Connect to remote host
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.140.128', username=ID, password=pwd,port=22)
        if "as" in ID:
            current_user = AS.AS(ID,client,pwd)
            current_user.menu()

        elif "ac" in ID:
            #current_user = AC.AC(ID,data[ID])
            pass#current_user.menu()
        elif "u" in ID:
            pass
        client.close()
        sys.exit(0)
    except IndexError:
        pass

authentication()
#clear()
#print("""

#""")


#json.dump(d,jfile)