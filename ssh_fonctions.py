import sys
import os
import paramiko

SitesID = {'paris':'1003','grenoble':'1004','strasbourg':'1005','rennes':'1006'}
IDSites = {'1003':'paris','1004':'grenoble','1005':'strasbourg','1006':'rennes'}      

    
def createUser(client,sudoPass, carac):
    group = ""
    if "A" in carac[0]:
        group = " -G sudo"
    command = f"sudo -S useradd -g {carac[4]}"+group+f" -c \"{carac[2]} {carac[1]}\" {carac[0]} && sudo chpasswd <<< {carac[0]}:{carac[3]}" 
    stdin , stdout, stderr = client.exec_command(command)
    stdin.write(sudoPass+'\n')
    stdin.flush()

def userListing(client, sites):
    listUsers = list()
    stdin , stdout, stderr = client.exec_command("cat /etc/passwd")
    users=stdout.read().decode().split('\n')[:-1]
    for user in users:
        if user.split(':')[3] in sites:
            listUsers.append(user)
    return listUsers

def userNameListing(client,sites):
    userList = userListing(client, sites)
    nameList = list()
    for user in userList:
        nameList.append(user.split(':')[0])
    return nameList

def passwordListing(client,sudoPass):
    passwordDict = dict()
    stdin , stdout, stderr = client.exec_command("sudo -S cat /etc/shadow")
    stdin.write(sudoPass+'\n')
    
    users=stdout.read().decode().split('\n')[:-1]
    for user in users:
        passwordDict[user.split(':')[0]]=user.split(':')[1]
    return passwordDict

def userSite(client, ID):
    userList = userListing(client, IDSites.keys())
    for user in userList:
        if ID in user.split(':')[0]:
            return user.split(':')[3]

def fileListing(client, path):
    stdin , stdout, stderr = client.exec_command("ls "+path)
    print(stdout.read().decode())

def logWrite(client, line, sudoPass = ""):
    sftp = client.open_sftp()
    try:
        sftp.open("/Projet/Logs/logs",'r')
        sftp.close()
    except:
        sftp.close()
        if sudoPass == "":
            return
        logReset(client,sudoPass)
    client.exec_command(f"echo {line}\n >> /Projet/Logs/logs")

def logReset(client, sudoPass):
    sftp = client.open_sftp()
    sftp.open("/Projet/Logs/logs",'w')
    sftp.close()
    stdin , stdout, stderr = client.exec_command("sudo -S chmod 777 /Projet/Logs/logs")
    stdin.write(sudoPass+'\n')
    
