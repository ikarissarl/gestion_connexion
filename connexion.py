import json
def identification():
    try:
        with open("date_base.json", "r") as f:
            mon_dictionnaire = json.load(f)
    except FileNotFoundError:
        mon_dictionnaire = []

    nom_utilisateur = input("entrez votre nom d'utilisateur ou votre addresse email :")
    password = input ("entrez votre mot de passe :")
    for i in mon_dictionnaire:
        if nom_utilisateur == i.get("username")  and password == i.get("pass") :
            print("="* 30)
            print(f"bienvenue {i.get("username")}")
            print("="*30)
            return True
        elif nom_utilisateur == i.get("email") and password == i.get("pass") :
            print("="* 30)
            print(f"bienvenue {i.get("username")}")
            print("="*30)
            return True
    
        else:
            print("nom d'utilisateur ou mot de pass incorrect")
            print("=" * 50)
            while True:
                question = input("voulez-vous ressayer ?(OUI/ NON) :")
                question = question.strip().upper()
                if question == "OUI":
                    identification()
                elif question == "NON":
                    return False
                

                else:
                    print("veuillez entrez une valeur valide")
                    continue
