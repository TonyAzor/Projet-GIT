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
    
    # Setup sftp connection and transmit this script
    #sftp = client.open_sftp()
    #sftp.put('./PortScanner.py', '/tmp/PortScanner.py')
    #sftp.close()

#client = paramiko.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect('192.168.140.128', username="as1", password="Lamortquitue94&&",port=22)
#print(passwordListing())