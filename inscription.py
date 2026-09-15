import json
def inscription():
    try:
        with open("date_base.json", "r") as f:
            mon_dictionnaire = json.load(f)
    except FileNotFoundError:
        mon_dictionnaire = []

    nom = input("quel est votre nom ? :")
    postnom = input("quel est votre postnom ? :")
    prenom = input("quel est votre prenom ? :")
    email = input("quel est votre email ? :")
    while True:
        genre = input("quel est votre genre ?(M/F) :")
        genre = genre.strip().upper()
        if genre == "M" or genre == "F":
            break
        else:
            print("veuillez entrer une valeur valide")
            continue
    while True:
        password = input("entrez un mot de pass:")
        if len(password) < 6:
            print("veuillez entrer un mot de passe comportant au moins 6 caracteres")
        else:
            break

        
    for i in mon_dictionnaire:
        
        while True:
            username = input("entrez un nom d'utilisateur:")
            if username == i.get("username"):
                print("nom d'utilisateur existant")
                print("veuillez choisir un nom d'utilisateur unique")
                continue
            else:
                break
        break

    user_info = {
        "nom": nom,
        "postnom" : postnom,
        "prenom" : prenom,
        "email" : email,
        "genre" : genre,
        "pass" : password,
        "username" : username}
    with open("date_base.json", "w") as f:
        mon_dictionnaire.append(user_info)
        json.dump(mon_dictionnaire, f, indent=4)
    print("loading...")
    print("compte cree avec succes")
    print(f"bienvenue {username}")



