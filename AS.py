from clear import clear
import json, hashlib, os, subprocess
from pprint import pprint
from threading import Thread
import PortScanner

class AS:
    ID = ""
    data = dict()
    user_file_path = "Projet-Python\\Users.json"

    def __init__(self, ID, data):
        self.ID = ID
        self.data = data
        

    
    def menu(self):
        clear()
        choice = input("""Veuillez choisir une action : 
1) Gestion des utilisateurs
2) Gestion du serveur ftp
3) Scan des ports
4) Simuler une attaque brute force
5) Ping
6) Quitter

""")
        if choice == '1':
            self.gestUsers()

        if choice == '3':
            self.scanPorts()

        if choice == '5':
            self.ping(input('\nVeuillez entrer un nom d\'hôte : '))
        if choice == '6':
            return

    def gestUsers(self):
        clear()

        choice = input("""Veuillez choisir une action :
1) Créer un utilisateur
2) Modifier un utilisateur
3) Supprimer un utilisateur
4) Lister les utilisateurs
5) Retour
6) Quitter

""")
        if choice == '1':
            self.createUser()
        if choice == '2':
            self.modifyUser()
        if choice == '3':
            self.deleteUser()
        if choice == '4':
            self.listingUser()
        if choice == '5':
            self.menu()
        if choice == '6':
            return

    def createUser(self):
        newID = ''
        ok =False
        while ok == False:
            clear()
            newID = input("""Veuillez choisir le type d'utilisateur : 
1) Utilisateur
2) Administrateur
3) Administrateur Suprème
4) Retour

""")
            if newID == '1':
                newID = 'U'
                ok = True
            elif newID == '2':
                newID = 'AC'
                ok = True
            elif newID == '3':
                newID = 'AS'
                ok = True
            elif newID == '4':
                self.gestUsers()
                return
            else : ok = False
        data = {
            "Nom": input("Nom : "),
            "Prénom":input("Prénom : "),
            "Hash": hashlib.sha256(input("Mot de passe provisoire : ").encode()).hexdigest(),
            "Location": input("Localisation : ")
        }
        fData = self.readData()
        hasID = False
        for user in reversed(fData.keys()):
            if newID == user[:len(newID)]:
                newID = ''.join([newID,str(int(user[len(newID):])+1)])
                hasID = True
                break
        if not hasID : 
            newID = ''.join([newID,'1'])
        fData.update({newID : data})
        self.writeData(fData)
        self.menu()
        return

    def scanPorts(self):
        clear()
        port = input("Entrez le port final (entre 1 et 65,535) que vous voulez scanner, entrez 'q' pour quitter : ")
        if port == 'q':
            self.menu()
            return
        if not port.isnumeric():
            self.scanPorts() 
            return
        if int(port) < 1 or int(port) > 65535:
            self.scanPorts() 
            return
        scan = Thread(target=PortScanner.scan,daemon=True, args=(port,))
        scan.start()
        #scan.join()
        input('\nScan des ports lancé, appuyez sur \"Entrer\" pour continuer')
        self.menu()
        return

    def ping(self, hostname):
        clear()
        response = os.system("ping " + hostname)
        if response == 0:
            print("\nNetwork Active")
        else:
            print("\nNetwork Error")
        input("Appuyer sur ENTRER pour revenir au menu")
        self.menu()
        return


    def deleteUser(self):
        clear()
        user = input('Veuillez entrer un User à supprimer : ').upper()
        fData = self.readData()
        if user in fData.keys():
            valid = ''
            while valid not in ['y','n']:
                valid = input(f'\nEtes-vous sûr de vouloir supprimer {user}?(y/n)').lower()
            if valid == 'n':
                self.gestUsers()
                return
            fData = self.readData()
            fData.pop(user)
            self.writeData(fData)
            input('Appuyer sur ENTRER pour revenir au menu')
            self.gestUsers()
            return
        else:
            input("Ce user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return

    def listingUser(self):
        clear()
        fData = self.readData()
        pprint(fData)
        input('Appuyer sur ENTRER pour revenir au menu')
        self.gestUsers()
        return

    def modifyUser(self):
        clear()
        user = input('Quel User voulez-vous modifier : ')
        fData = self.readData()
        if user.upper() in fData.keys():
            clear()
            choice = input("""Que voulez-vous modifier : 
1) Nom
2) Prénom
3) Mot de passe
4) Localisation
5) Retour

""")    
            if choice == '5':
                self.gestUsers()
                return
            choiceList = ['','Nom', 'Prénom','', 'Location']
            if choice == '3':
                fData[user]['Hash'] = hashlib.sha256(input("\nMot de passe provisoire : ").encode()).hexdigest()
            else:
                fData[user][choiceList[int(choice)]] = input("\nEntrez la nouvelle valeur : ")
            self.writeData(fData)
            self.gestUsers()
            return
        else:
            input("\nCe user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return
    
    def writeData(self,fData):
        f = open(self.user_file_path, 'w')
        json.dump(fData,f,indent=4)
        f.close()
    
    def readData(self):
        f = open(self.user_file_path, 'r')
        fData = json.load(f)
        f.close()
        return fData