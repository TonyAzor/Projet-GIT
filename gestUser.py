import json, os, hashlib, pprint, getpass
import AS
from clear import clear


user_file_path = "Projet-Python\\Users.json"
userFile = open(user_file_path, 'r')
data = json.load(userFile)
userFile.close()

current_user = None

def reloadJson():
    userFile = open(user_file_path, 'r')
    data = json.load(userFile)
    userFile.close()

def write(data):
    reloadJson()
    userFile = open(user_file_path, 'w')
    json.dump(data, userFile)
    userFile.close()

def authentication():
    reloadJson()
    ID = input("Veuillez entrer votre ID : ").upper()
    pwd = hashlib.sha256(getpass.getpass("Veuillez entrer votre mot de passe : ").encode()).hexdigest()
    if ID not in data.keys():
        print('Utilisateur introuvable')
        authentication()
        return
    elif "AS" in ID:
        if data[ID]["Hash"] == pwd:
            print(f"Admin Suprème {ID} connecté")
            current_user = AS.AS(ID,data[ID])
            current_user.menu()
        else:
            input("Pas le bon mot de passe appuyez sur Entrer pour recommencer")
            authentication()
            return

    elif "AC" in ID:
        if data[ID]["Hash"] == pwd:
            print(f"Admin Suprème {ID} connecté")
            current_user = AC.AC(ID,data[ID])
            current_user.menu()
        else:
            input("Pas le bon mot de passe appuyez sur Entrer pour recommencer")
            authentication()
            return
    elif "U" in ID:
        if data[ID]["Hash"] == pwd:
            print(f"Admin Suprème {ID} connecté")
        else:
            input("Pas le bon mot de passe appuyez sur Entrer pour recommencer")
            authentication()
            return


authentication()
#clear()
#print("""

#""")


#json.dump(d,jfile)