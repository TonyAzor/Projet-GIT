from clear import clear
import os
from threading import Thread
import ssh_fonctions,BruteForce
from datetime import datetime

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
6) Gestion des logs
7) Quitter

""")
        if choice == '1':
            self.gestUsers()
        elif choice == '2':
            self.ftpMenu()
        elif choice == '3':
            self.scanPorts()
        elif choice == '4':
            self.bruteForceMenu()
        elif choice == '5':
            self.ping(input('\nVeuillez entrer un nom d\'hôte : '))
        elif choice == '6':
            self.logsMenu()
        elif choice == '7':
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
        elif choice == '2':
            self.modifyUser()
        elif choice == '3':
            self.deleteUser()
        elif choice == '4':
            self.listingUser()
        elif choice == '5':
            self.menu()
        elif choice == '6':
            return
        else:
            self.gestUsers()
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
        for user in reversed(ssh_fonctions.userNameListing(self.client,ssh_fonctions.IDSites.keys())):
            if newID == user[:len(newID)] and user[len(newID):].isnumeric():
                newID = ''.join([newID,str(int(user[len(newID):])+1)])
                hasID = True
                break
        if not hasID : 
            newID = ''.join([newID,'1'])
        ssh_fonctions.createUser(self.client,self.sudoPass,[newID,lastname,firstname,pwd,site])
        ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a créé l'user {newID} s'appelant {firstname} {lastname} dans le site de {site}",self.sudoPass)
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
            input("Vous n'avez pas mis \"-\" entre les deux port ou vous n'avez pas mis le bon nombre de ports")
            self.scanPorts() 
            return
        if int(ports[0]) < 1 or int(ports[0])>int(ports[1]) or int(ports[1]) > 65535:
            input("vous n'avez pas respecté la règle : entre 1 et 65,535 au format \"port1-port2\" avec port1<=port2")
            self.scanPorts() 
            return
        sftp = self.client.open_sftp()
        self.client.exec_command(f'touch /Projet/Scan/{ports[0]}-{ports[1]}.scan')
        sftp.remove("/Projet/Scan/portScanLogs.txt")
        sftp.close()
        ssh_fonctions.logWrite(self.client,datetime.now()+f"{self.ID} lancé un scan des ports",self.sudoPass)
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

        if user in reversed(ssh_fonctions.userNameListing(self.client,ssh_fonctions.IDSites.keys())):
            valid = ''
            while valid not in ['y','n']:
                valid = input(f'\nEtes-vous sûr de vouloir supprimer {user}?(y/n)').lower()
            if valid == 'n':
                self.gestUsers()
                return
            stdin , stdout, stderr = self.client.exec_command(f'sudo -S deluser {user}')
            stdin.write(self.sudoPass+'\n')
            stdin.flush()
            ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a supprimé l'user {user}",self.sudoPass)
            input('Appuyer sur ENTRER pour revenir au menu')
            self.gestUsers()
            return
        else:
            input("Ce user n'existe pas, appuyez sur \"entrer\" pour continuer")
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
            site=ssh_fonctions.IDSites.keys()
        elif choice == '2':
            site=[ssh_fonctions.SitesID['paris']]
        elif choice == '3':
            site=[ssh_fonctions.SitesID['grenoble']]
        elif choice == '4':
            site=[ssh_fonctions.SitesID['strasbourg']]
        elif choice == '5':
            site=[ssh_fonctions.SitesID['rennes']]
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
        ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a demandé une liste des users",self.sudoPass)
        input('\nAppuyer sur ENTRER pour revenir au menu')
        self.gestUsers()
        return

    def modifyUser(self):
        clear()
        user = input('Quel User voulez-vous modifier : ')
        if user.upper() in reversed(ssh_fonctions.userNameListing(self.client,ssh_fonctions.IDSites.keys())):
            clear()
            choice = input("""Que voulez-vous modifier : 
1) Nom et prénom
2) Mot de passe
3) Site
4) Retour\n\n""")    
            if choice == '1':
                newName = input("Veuillez entrer le nouveau nom ET prénom, entrez 'q' pour revenir : ")
                if newName == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S usermod -c \"{newName}\" {user}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()  
                ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a mofifié les nom et prénom de l'user {user}",self.sudoPass)  
                
            elif choice == '2':
                newPassword = input("Veuillez entrer le nouveau mot de passe, entrez 'q' pour revenir : ")
                if newPassword == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S chpasswd <<< {user}:{newPassword}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()    
                ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a modifié le mot de passe de l'user {user}",self.sudoPass)
            elif choice == '3':
                newGroup = input("Veuillez entrer le nouveau groupe, entrez 'q' pour revenir : ")
                if newName == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S usermod -g {newGroup} {user}"
                if "a" in user.lower():
                    command += " -G sudo"
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()
                ssh_fonctions.logWrite(self.client,datetime.now()+f"{self.ID} a déplacé l'user {user} au site de {newGroup}",self.sudoPass)  
            elif choice == '4':
                self.gestUsers()
                return
            else:
                self.modifyUser()
                return
            self.gestUsers()
            return
            

        else:
            input("\nCe user n'existe pas, appuyez sur \"entrer\" pour continuer")
        self.gestUsers()
        return
    
    def bruteForceMenu(self):
        clear()
        user = input('De quel user souhaitez vous brute force le mot de passe ? "q" pour quitter : ')
        if user == "q":
            self.menu()
            return
        length = input('\nQuelle taille max voulez-vous tester ? "q" pour quitter : ')
        if length == "q":
            self.menu()
            return
        pwdDict = ssh_fonctions.passwordListing(self.client,self.sudoPass)
        if user in pwdDict.keys():
            scanThread = Thread(target=BruteForce.bruteForce,daemon=True, args=("", int(length), pwdDict[user].split('$')[2], pwdDict[user], user,self.client))
            scanThread.start()
        ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a lancé un brute force sur le mot de passe de {user}",self.sudoPass)
        input(f"\nLe brute force a été lancé sur le mot de passe de {user}, veuillez ne pas fermer l'application pour ne pas arrêter le processus.")
        self.menu()
        return
        
    def ftpMenu(self):
        clear()
        site = input("""Veuillez choisir un site : 
1) Paris
2) Strasbourg
3) Rennes
4) Grenoble
5) Retour\n\n""")
        if site == "5":
            self.menu()
            return
        if site in [str(i) for i in range(1,5)]:
            siteList = ["","paris","strasbourg","rennes","grenoble"]
            self.siteFtpMenu(siteList[int(site)])
            return
        self.ftpMenu()
        return
        

    def siteFtpMenu(self,site):
        clear()
        aType = input("""Veuillez indiquer quel est le type d'audit que vous souhaitez voir :
1) Comptable
2) Contractuel
3) Environnement
4) Interne
5) Légal
6) Organisationnel
7) Retour

""")    
        typeList = ["","comptable","contractuel","environnement","interne","legal","organisationnel"]
        if aType == "7":
            self.ftpMenu()
            return
        elif aType in [str(i) for i in range(1,7)]:
            self.auditFtpMenu(site,typeList[int(aType)])
            return
        else:
            self.siteFtpMenu(site)
            return

    def auditFtpMenu(self,site,aType,archives = ""):
        clear()
        ssh_fonctions.fileListing(self.client,f"/Projet/Audits/{site}/{aType}/{archives}")
        action = input("""Que voulez-vous faire ?
1) Archiver
2) Copier
3) Télécharger
4) Supprimer
5) Accéder aux archives
6) Retour\n\n""")
        if action =="6":
            if archives == "archives/":
                self.auditFtpMenu(site,aType,"")
                return
            self.siteFtpMenu(site)
            return
        elif action == "1":
            files = input("Entrez le ou les noms (séparés par une \",\") des fichiers à archiver : \n\n")
            for f in files.split(","):
                self.client.exec_command(f"mv /Projet/Audits/{site}/{aType}/{archives}{f} /Projet/Audits/{site}/{aType}/archives")
            ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a archivé les fichiers {files} du site de {site} dans le répertoire d'audit {aType}",self.sudoPass)
            input("Les fichiers ont été archivés")
        elif action == "2":
            files = input("Entrez le ou les noms (séparés par une \",\") des fichiers à copier : \n\n")
            newNames = input("\n\nEntrez le ou les nouveaux noms (avec les extensions et séparés par une \",\") des fichiers à copier : \n\n")
            if len(files.split(",")) != len(newNames.split(",")):
                input("Il n'y a pas le même nombres de nouveaux noms que de fichiers")
                self.auditFtpMenu(site,aType,archives)
                return
            for i in range(len(files.split(","))):
                f = files.split(",")[i]
                n = newNames.split(",")[i]
                self.client.exec_command(f"cp /Projet/Audits/{site}/{aType}/{archives}{f} /Projet/Audits/{site}/{aType}/{archives}{n}")
            ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a copié les fichiers {files} appelés {newNames} du site de {site} dans le répertoire d'audit {aType}",self.sudoPass)
            input("Les fichiers a été copiés")
        elif action == "3":
            try:
                files = input("Entrez le ou les noms (séparés par une \",\") des fichiers à télécharger : \n\n")
                sftp = self.client.open_sftp()
                for f in files.split(","):
                    sftp.get(f"/Projet/Audits/{site}/{aType}/{archives}{f}",f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\{f}")
                sftp.close()
                ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a téléchargé les fichiers {files} du site de {site} dans le répertoire d'audit {aType}",self.sudoPass)
                input("Les fichiers ont été téléchargés")
            except IOError as e:
                input(e)
        elif action == "4":
            files = input("Entrez le ou les noms (séparés par une \",\") des fichiers à supprimer : \n\n")
            for f in files.split(","):
                self.client.exec_command(f"rm /Projet/Audits/{site}/{aType}/{archives}{f}")
            ssh_fonctions.logWrite(self.client,datetime.now()+f"  {self.ID} a supprimé les fichiers {files} du site de {site} dans le répertoire d'audit {aType}",self.sudoPass)
            input("Les fichiers ont été supprimé")    
            
        elif action == "5":
            archives = "archives/"
        self.auditFtpMenu(site,aType,archives)
        return

    def logsMenu(self):
        clear()
        action = input("""Que voulez-vous faire :
1) Lire le fichier
2) Réinitialiser le fichier
3) Télécharger le fichier
4) Retour
5) Quitter\n\n""")
        if action == '1':
            stdin , stdout, stderr = self.client.exec_command("cat /Projet/Logs/logs")
            input(stdout.read().decode())
        elif action == '2':
            ssh_fonctions.logReset(self.client,self.sudoPass)
            input("Le fichier a été réinitialisé")
        elif action == '3':
            try:
                sftp = self.client.open_sftp()
                sftp.get(f"/Projet/Logs/logs",f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\logs")
                sftp.close()
                input("Le fichier a été téléchargé")
            except IOError as e:
                input(e)
        elif action == '4':
            self.menu()
            return
        elif action == '5':
            return 
        self.logsMenu()
        return

