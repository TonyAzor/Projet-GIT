import clear
import hashlib

liste = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','&','%']

def bruteForce(word, length, hashWord):
    if length > 0:
        for letter in liste:
            
            print(word+letter)
            if hashlib.sha256((word+letter).encode()).hexdigest() == hashWord:
                print('Le mot de passe est trouvé et est : '+word+letter)
                return 0
            else:
                if bruteForce(word+letter,length-1,hashWord) == 0:
                    return 0
    return 1


bruteForce('',4,'9058f79c893a1d7e20b13009b95b9cf3211478a91a47e2ad65bdfedad6fc98f4')