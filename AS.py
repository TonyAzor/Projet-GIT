from clear import clear
import json, hashlib, os, subprocess
from pprint import pprint
from threading import Thread
import ssh_fonctions,BruteForce

class AS:
    ID = ""
    client = None
    sudoPass = ""

    def __init__(self, ID,sshClient,sudoPass):
        self.ID = ID
        self.client = sshClient
        self.sudoPass=sudoPass
        

    
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
        if choice == '4':
            self.bruteForceMenu()

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
        clear()
        newID = input("""Veuillez choisir le type d'utilisateur : 
1) Utilisateur
2) Administrateur
3) Administrateur Suprème
4) Retour

""")
        if newID == '1':
            newID = 'U'
        elif newID == '2':
            newID = 'AC'
        elif newID == '3':
            newID = 'AS'
        elif newID == '4':
            self.gestUsers()
            return
        else : 
            self.createUser()
            return
        lastname = input("Nom : ")
        firstname = input("Prénom : ")
        pwd = input("Mot de passe provisoire : ")
        site = input("Site : ")
        hasID = False
        for user in reversed(ssh_fonctions.userNameListing(self.client,[list(ssh_fonctions.SitesID.values())])):
            if newID == user[:len(newID)] and user[len(newID):].isnumeric():
                newID = ''.join([newID,str(int(user[len(newID):])+1)])
                hasID = True
                break
        if not hasID : 
            newID = ''.join([newID,'1'])
        ssh_fonctions.createUser(self.client,self.sudoPass,[newID,lastname,firstname,pwd,site])
        self.menu()
        return

    def scanPorts(self):
        clear()
        plage = input("Entrez la plage de ports (entre 1 et 65,535 au format \"port1-port2\" avec port1<=port2) que vous voulez scanner, entrez 'q' pour quitter : ")
        if plage == 'q':
            self.menu()
            return
        ports = plage.split("-")
        if len(ports)!=2:
            self.scanPorts() 
            return
        if int(ports[0]) < 1 or int(ports[0])>int(ports[1]) or int(ports[1]) > 65535:
            self.scanPorts() 
            return
        sftp = self.client.open_sftp()
        self.client.exec_command(f'touch /Projet/Scan/{ports[0]}-{ports[1]}.scan')
        sftp.remove("/Projet/Scan/portScanLogs.txt")
        sftp.close()
        
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

        if user in reversed(ssh_fonctions.userNameListing(self.client,[list(ssh_fonctions.SitesID.values())])):
            valid = ''
            while valid not in ['y','n']:
                valid = input(f'\nEtes-vous sûr de vouloir supprimer {user}?(y/n)').lower()
            if valid == 'n':
                self.gestUsers()
                return
            stdin , stdout, stderr = self.client.exec_command(f'sudo -S deluser {user}')
            stdin.write(self.sudoPass+'\n')
            stdin.flush()
            input('Appuyer sur ENTRER pour revenir au menu')
            self.gestUsers()
            return
        else:
            input("Ce user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return

    def listingUser(self):
        clear()
        choice = input("""Quel site voulez-vous lister : 
1) Tous
2) Paris
3) Grenoble
4) Strasbourg
5) Rennes
6) Retour

""")    
        site = list()
        if choice == '1':
            site.append(list(ssh_fonctions.SitesID.values()))
        elif choice == '2':
            site.append([ssh_fonctions.SitesID['paris'],None])
        elif choice == '3':
            site.append([ssh_fonctions.SitesID['grenoble'],None])
        elif choice == '4':
            site.append([ssh_fonctions.SitesID['strasbourg'],None])
        elif choice == '5':
            site.append([ssh_fonctions.SitesID['rennes'],None])
        else : 
            self.createUser()
            return
        clear()
        users = ssh_fonctions.userListing(self.client,site)
        if len(users)==0:
            print('Aucun user ou admin dans ce site\n')
        for user in users:
            infos = user.split(':')
            print(infos[0]+'\t'+infos[4]+'\t'+ssh_fonctions.IDSites[infos[3]]+'\n')
        input('\nAppuyer sur ENTRER pour revenir au menu')
        self.gestUsers()
        return

    def modifyUser(self):
        clear()
        user = input('Quel User voulez-vous modifier : ')
        if user.upper() in reversed(ssh_fonctions.userNameListing(self.client,[list(ssh_fonctions.SitesID.values())])):
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
                pass#fData[user]['Hash'] = hashlib.sha256(input("\nMot de passe provisoire : ").encode()).hexdigest()
            else:
                pass#fData[user][choiceList[int(choice)]] = input("\nEntrez la nouvelle valeur : ")

            self.gestUsers()
            return
        else:
            input("\nCe user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return
    
    def bruteForceMenu(self):
        clear()
        user = input('De quel user souhaitez vous brute force le mot de passe ? "q" pour quitter ')
        if user == "q":
            self.menu()
            return
        length = input('\nQuelle taille max voulez-vous tester ? "q" pour quitter ')
        if length == "q":
            self.menu()
            return
        pwdDict = ssh_fonctions.passwordListing(self.client,self.sudoPass)
        if user in pwdDict.keys():
            scanThread = Thread(target=BruteForce.bruteForce,daemon=True, args=("", int(length), pwdDict[user].split('$')[2], pwdDict[user], user,self.client))
            scanThread.start()
        input(f"\nLe brute force a été lancé sur le mot de passe de {user}, veuillez ne pas éteindre l'application pour ne pas arrêter le processus.")
        self.menu()
        return
        