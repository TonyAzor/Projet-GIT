import clear
from passlib.hash import sha512_crypt as sha512

liste = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','&','%','$','@']

def bruteForce(word,length, salt, shadow, user, client):
    if length > 0:
        for letter in liste:
            if sha512.using(salt=salt).hash(word+letter, rounds=5000) == shadow:
                sftp = client.open_sftp()
                sftp.open('/Projet/Bruteforce/password','w')
                sftp.close
                client.exec_command(f'echo "Le mot de passe du user {user} est '+word+letter+'" >> /Projet/Bruteforce/password')
                return 0
            else:
                if bruteForce(word+letter, length-1, salt, shadow, user, client) == 0:
                    return 0
    return 1

