import json, os, hashlib, pprint, getpass
import AS
from clear import clear


user_file_path = "C:\\Users\\Tony\\Documents\\Github\\Projet-Python\\Users.json"

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
            print("Erreur")
    elif "AC" in ID:
        if data[ID]["Hash"] == pwd:
            print(f"Admin Suprème {ID} connecté")
        else:
            print("Erreur")
    elif "U" in ID:
        if data[ID]["Hash"] == pwd:
            print(f"Admin Suprème {ID} connecté")
        else:
            print("Erreur")

def menuAS():
    clear()
    print("""Veuillez choisir une action : 
1) Gestion des utilisateurs
2) Gestion du serveur ftp
3) Scan des ports
4) Simuler une attaque brute force
5) Ping
6) Quitter

""")

    clear()
    print("""1) Gérer les administrateurs
2) Gérer les utilisateurs
3) Retour
4) Quitter

""")

def menuAC():
    clear()
    print("""Veuillez choisir une action : 
    1) Gestion des utilisateurs
    2) Gestion du serveur ftp
    4) Retour
    5) Quitter
    
    """)

def menuU():
    clear()
    print('a')  


def gestUsers(ID):
    clear()
    if 'A' in ID:
        print("""1) Créer un utilisateur
        2) Modifier un utilisateur
        3) Supprimer un utilisateur
        4) Lister les utilisateurs
        5) Retour
        6) Quitter
        
        """)

authentication()
#clear()
#print("""

#""")


#json.dump(d,jfile)