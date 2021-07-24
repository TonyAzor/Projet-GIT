import clear
from passlib.hash import sha512_crypt as sha512

liste = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','&','%','$','@']

def bruteForce(word, salt, length, hashWord):
    if length > 0:
        for letter in liste:
            if sha512.using(salt=salt).hash(word, rounds=5000) == hashWord:
                print('Le mot de passe est trouvé et est : '+word+letter)
                return 0
            else:
                if bruteForce(word+letter,salt,length-1,hashWord) == 0:
                    return 0
    return 1

