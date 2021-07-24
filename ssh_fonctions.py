import sys
import os
import paramiko

SitesID = {'paris':'1003','grenoble':'1004','strasbourg':'1005','rennes':'1006'}
IDSites = {'1003':'paris','1004':'grenoble','1005':'strasbourg','1006':'rennes'}      

    
def createUser(client,sudoPass, carac):
    command = f"sudo -S useradd -g {carac[4]} -c \"{carac[2]} {carac[1]}\" {carac[0]} && sudo chpasswd <<< {carac[0]}:{carac[3]}"
    
    print("Executing {}".format( command ))
    stdin , stdout, stderr = client.exec_command(command)
    stdin.write(sudoPass+'\n')
    stdin.flush()
    print(stdout.read())
    print( "Errors")
    print(stderr.read())

def userListing(client, sites):
    listUsers = list()
    stdin , stdout, stderr = client.exec_command("cat /etc/passwd")
    users=stdout.read().decode().split('\n')[:-1]
    for user in users:
        if user.split(':')[3] in sites[0]:
            listUsers.append(user)
    return listUsers

def userNameListing(client,sites):
    userList = listingUser(client, sites)
    nameList = list()
    for user in userList:
        nameList.append(user.split(':')[0])
    return nameList

def passwordListing(client,sudoPass):
    passwordDict = dict()
    stdin , stdout, stderr = client.exec_command("cat /etc/shadow")
    stdin.write(sudoPass+'\n')
    users=stdout.read().decode().split('\n')[:-1]
    for user in users:
        passwordDict[user.split(':')[0]]=user.split(':')[1]
    return listUsers
    
    # Setup sftp connection and transmit this script
    #sftp = client.open_sftp()
    #sftp.put('./PortScanner.py', '/tmp/PortScanner.py')
    #sftp.close()
