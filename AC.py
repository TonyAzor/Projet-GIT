from clear import clear
import json, hashlib, os
from pprint import pprint

class AC:
    ID = ""
    data = dict()
    user_file_path = "Projet-Python\\Users.json"

    def __init__(self, ID, data):
        self.ID = ID
        self.data = data
        
    def getLocation(self):
        return self.data['Location']
    
    def menu(self):
        clear()
        choice = input("""Veuillez choisir une action : 
1) Gestion des utilisateurs
2) Gestion du serveur ftp
3) Quitter

""")
        if choice == '1':
            self.gestUsers()

        if choice == '3':
            return
        else:
            self.menu()
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
        clear()
        data = {
            "Nom": input("Nom : "),
            "Prénom":input("Prénom : "),
            "Hash": hashlib.sha256(input("Mot de passe provisoire : ").encode()).hexdigest(),
            "Location": self.getLocation
        }
        fData = self.readData()
        newID = ''
        for user in reversed(fData.keys()):
            if 'U' == user[0]:
                newID = ''.join(['U',str(int(user[1:])+1)])
                break
            else : 
                newID = 'U1'
        fData.update({newID : data})
        self.writeData(fData)
        self.gestUsers()
        return

    def modifyUser(self):
        clear()
        user = input('Quel User voulez-vous modifier : ')
        fData = self.readData()
        if user in fData.keys():
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
            choiceList = ['Nom', 'Prénom','', 'Location']
            if choice == '3':
                password = hashlib.sha256()
                password.update(input("Mot de passe provisoire : ").encode())
                fData[user]['Hash'] = password.hexdigest()
            else:
                fData[user][choiceList[int(choice)]] = password.hexdigest()
            self.gestUsers()
            return
        else:
            input("Ce user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return
        
    def deleteUser(self):
        clear()
        user = input('Veuillez entrer un User à supprimer : ').upper()
        fData = self.readData()
        if user in fData.keys() and self.getLocation() == fData[user]['Location']:
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

    def writeData(self,fData):
        f = open(self.user_file_path, 'w')
        json.dump(fData,f,indent=4)
        f.close()
    
    def readData(self):
        f = open(self.user_file_path, 'r')
        fData = json.load(f)
        f.close()
        return fData