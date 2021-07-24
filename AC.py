from clear import clear
import random, os
import ssh_fonctions, BruteForce
from datetime import datetime

class AC:
    ID = ""
    client = None
    sudoPass = ""
    Site = ""

    def __init__(self, ID,sshClient,sudoPass):
        self.ID = ID
        self.client = sshClient
        self.sudoPass=sudoPass
        self.Site = ssh_fonctions.userSite(sshClient,ID)
        

    
    def menu(self):
        clear()
        choice = input("""Veuillez choisir une action : 
1) Gestion des utilisateurs
2) Gestion du serveur ftp
3) Quitter

""")
        if choice == '1':
            self.gestUsers()
            return
        if choice == '2':
            self.auditMenu()
            return
        elif choice == '3':
            return
        self.menu()
        return


    def gestUsers(self):
        clear()
        print(self.Site)
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
2) Retour

""")
        if newID == '1':
            newID = 'U'
        elif newID == '4':
            self.gestUsers()
            return
        else : 
            self.createUser()
            return
        clear()
        lastname = input("Nom : ")
        firstname = input("Prénom : ")
        pwd = ""
        for i in range(4):
            pwd += random.choice(BruteForce.liste)
        site = self.Site
        hasID = False
        for user in reversed(ssh_fonctions.userNameListing(self.client,[self.Site])):
            if newID == user[:len(newID)] and user[len(newID):].isnumeric():
                newID = ''.join([newID,str(int(user[len(newID):])+1)])
                hasID = True
                break
        if not hasID : 
            newID = ''.join([newID,'1'])
        ssh_fonctions.createUser(self.client,self.sudoPass,[newID,lastname,firstname,pwd,site])
        ssh_fonctions.logWrite(self.client,f"{self.ID} a créé l'user {newID} s'appelant {firstname} {lastname} dans le site de {site}")
        input(f"L'user {newID} s'appelant {firstname} {lastname} a été créé dans le site de {site}")
        self.menu()
        return


    def deleteUser(self):
        clear()
        user = input('Veuillez entrer un User à supprimer : ').upper()

        if user in reversed(ssh_fonctions.userNameListing(self.client,[self.Site])):
            valid = ''
            while valid not in ['y','n']:
                valid = input(f'\nEtes-vous sûr de vouloir supprimer {user}?(y/n)').lower()
            if valid == 'n':
                self.gestUsers()
                return
            stdin , stdout, stderr = self.client.exec_command(f'sudo -S userdel --force -r {user}')
            stdin.write(self.sudoPass+'\n')
            stdin.flush()
            input(f"L'user {user} a été supprimé")
            ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a supprimé l'user {user}")
            self.gestUsers()
            return
        else:
            input("Ce user n'existe pas ou ne fait pas parti de votre site, appuyez sur \"entrer\" pour continuer")
            self.gestUsers()
            return

    def listingUser(self):
        clear()
        users = ssh_fonctions.userListing(self.client,[self.Site])
        if len(users)==0:
            print('Aucun user ou admin dans ce site\n')
        for user in users:
            infos = user.split(':')
            print(infos[0]+'\t'+infos[4]+'\t'+ssh_fonctions.IDSites[infos[3]]+'\n')
        input('\nAppuyer sur ENTRER pour revenir au menu')
        ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a demandé une liste des users")
        self.gestUsers()
        return

    def modifyUser(self):
        clear()
        user = input('Quel User voulez-vous modifier : ')
        if user.upper() in reversed(ssh_fonctions.userNameListing(self.client,[self.Site])):
            clear()
            choice = input("""Que voulez-vous modifier : 
1) Nom et prénom
2) Mot de passe
3) Site
4) Retour

""")    
            if choice == '1':
                newName = input("Veuillez entrer le nouveau nom ET prénom, entrez 'q' pour revenir : ")
                if newName == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S usermod -c \"{newName}\" {user}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()     
                ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a mofifié les nom et prénom de l'user {user}")
                input(f"Le nom de {user} a été modifié")
            if choice == '2':
                newPassword = input("Veuillez entrer le nouveau mot de passe, entrez 'q' pour revenir : ")
                if newPassword == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S ls && sudo chpasswd <<< {user}:{newPassword}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()   
                ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a modifié le mot de passe de l'user {user}") 
                input(f"Le mot de passe de {user} a été modifié")
            if choice == '3':
                newGroup = input("Veuillez entrer le nouveau groupe, entrez 'q' pour revenir : ")
                if newName == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S usermod -g {newGroup} {user}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()
                ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"{self.ID} a déplacé l'user {user} au site de {newGroup}")  
                input(f"Le site de {user} a été modifié")
            if choice == '4':
                self.gestUsers()
                return
            else:
                self.modifyUser()
                return
        else:
            input("\nCe user n'existe pas, appuyez sur \"entrer\" pour continuer")
        self.gestUsers()
        return
    
    def auditMenu(self):
        clear()
        aType = input(""""Veuillez indiquer quel est le type d'audit que vous souhaitez envoyer :
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
            self.menu()
            return
        elif aType in [str(i) for i in range(1,7)]:
            self.actionAuditMenu(typeList[int(aType)])
            return
        else:
            self.auditMenu()
            return
        
    def actionAuditMenu(self,aType):
        clear()
        ssh_fonctions.fileListing(self.client,f"/Projet/Audits/{self.Site}/{aType}/")
        action = input("""veuikllez sélectionner l'action que vous voulez faire :
1) Uploader
2) Télécharger
3) Retour\n\n""")
        if action == '1':
            aFile = input("Veuillez glissez le fichier dans le terminal : \n\n")
            try:
                open(aFile,'r')
            except:
                input("Le chemin du fichier n'est pas valide")
                self.actionAuditMenu(aType)
                return
            sftp = self.client.open_sftp()
            sftp.put(aFile,"/Projet/Audits/"+str(ssh_fonctions.IDSites[self.Site])+"/"+aType+"/"+aFile.split("\\")[-1])
            sftp.close()
            ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a uploadé le fichier {aFile} au site de {str(ssh_fonctions.IDSites[self.Site])} dans le répertoire d'audit {aType}")
            input("Le fichier a été envoyé")
            self.menu()
            return
        elif action == '2':
            try:
                files = input("Entrez le ou les noms (séparés par une \",\") des fichiers à télécharger : \n\n")
                sftp = self.client.open_sftp()
                for f in files.split(","):
                    sftp.get(f"/Projet/Audits/{str(ssh_fonctions.IDSites[self.Site])}/{aType}/{f}",f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\{f}")
                sftp.close()
                ssh_fonctions.logWrite(self.client,datetime.now().isoformat(timespec='seconds')+f"  {self.ID} a téléchargé les fichiers {files} du site de {str(ssh_fonctions.IDSites[self.Site])} dans le répertoire d'audit {aType}",self.sudoPass)
                input("Les fichiers ont été téléchargés")
            except IOError as e:
                input(e)
        elif action == '3':
            self.auditMenu()
            return    