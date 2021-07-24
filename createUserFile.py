import json, os, hashlib

user_file_path = "C:\\Users\\Tony\\Documents\\Github\\Projet-Python\\Users.json"

mdp = hashlib.sha256()

mdp.update(input("Enter your AS password :").encode())

with open(user_file_path, 'w') as jfile:
    data = {
        "AS1" : {
            "Nom": "ROSA",
            "Prénom":"Tony",
            "Hash": mdp.hexdigest(),
            "Location": "Paris"
        }
    }

    json.dump(data,jfile, indent = 4)