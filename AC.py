from clear import clear
import ssh_fonctions

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
            self.auditPut()
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
        lastname = input("Nom : ")
        firstname = input("Prénom : ")
        pwd = input("Mot de passe provisoire : ")
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
        users = ssh_fonctions.userListing(self.client,[self.Site])
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
                
            if choice == '2':
                newPassword = input("Veuillez entrer le nouveau mot de passe, entrez 'q' pour revenir : ")
                if newPassword == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S chpasswd <<< {user}:{newPassword}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()    
            if choice == '3':
                newGroup = input("Veuillez entrer le nouveau groupe, entrez 'q' pour revenir : ")
                if newName == 'q':
                    self.gestUsers()
                    return
                command = f"sudo -S usermod -g {newGroup} {user}" 
                stdin , stdout, stderr = self.client.exec_command(command)
                stdin.write(self.sudoPass+'\n')
                stdin.flush()  
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
    
    def auditPut(self):
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
            aFile = input("Veuillez glissez le fichier dans le terminal : \n\n")
            try:
                open(aFile,'r')
            except:
                input("Le chemin du fichier n'est pas valide")
                self.auditPut()
                return
            sftp = self.client.open_sftp()
            sftp.put(aFile,"/Projet/Audits/"+str(ssh_fonctions.IDSites[self.Site])+"/"+typeList[int(aType)]+"/"+aFile.split("\\")[-1])
            sftp.close()
            input("Le fichier a été envoyé")
            self.menu()
            return
        else:
            self.auditPut()
            return
        