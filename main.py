import connexion
import inscription
import json

if __name__=="__main__":
    
    print("1. connexion \n2. creation de compte")
    chemin = "date_base.json"
    while True:
        try:
            option = int(input("Quelle option choisissez-vous ?(1 ou 2) : "))
            if option == 1 or option == 2:
                break
            else:
                continue
        except ValueError :
            print("veuillez entrer une valeur valide (1 ouo 2)")
            continue

    if option == 1:
        connexion.identification()
    else:
        inscription.inscription()
    

