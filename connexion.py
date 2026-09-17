import smtplib
from faker import Faker
import json
from email.message import EmailMessage

fake = Faker(locale="fr_FR")
json_file = open("mail_config.json")
cfg = json.load(json_file)
message = fake.numerify(text="%%%%%%")
msg = EmailMessage()

def identification():
    try:
        with open("date_base.json", "r") as f:
            mon_dictionnaire = json.load(f)
    except FileNotFoundError:
        mon_dictionnaire = []

    while True:

        nom_utilisateur = input("entrez votre nom d'utilisateur ou votre addresse email :")
        password = input ("entrez votre mot de passe :")
        for i in mon_dictionnaire:
            if nom_utilisateur == i.get("username") or nom_utilisateur == i.get("email") and password == i.get("pass") :
                print("="* 30)
                print(f"bienvenue {i.get("username")}")
                print("="*30)
                return True
    
        
    
        print("nom d'utilisateur ou mot de pass incorrect")
        print("=" * 50)
        mot_de_passe_oublie = input("avez-vous oublie votre mot de passe ?(oui ou non) :")
        while True:
            if mot_de_passe_oublie.lower() == "oui":
                email = input("entrez votre email :")
                for i in mon_dictionnaire:
                    if email == i.get("email"):
                        msg["to"] = i.get("email")
                        msg["from"] = cfg["gmail"]
                        msg["subject"] = "mail de verification"
                        msg.set_content(f"le code de verification est {message}")
                        try:
                            with smtplib.SMTP_SSL(cfg["serveur"], cfg["port"]) as smtp:
                                smtp.login(cfg["gmail"], cfg["pwd"])
                                smtp.send_message(msg)
                                print("code envoye")
                                while True:
                                    verification_message = input("veuillez entrer le code a 6 chiffres qui vous est envoye:")
                                    if verification_message == message :
                                        print("code correct email valide")
                                        break
                                    else:
                                        print("code incorrect veuillez reessayer")
                                        continue
                            break
                        except smtplib.SMTPRecipientsRefused:
                            print("email incorrect, veuillez verifier votre email")
                            continue
                        except smtplib.SMTPException:
                            print("une erreur est survenue lors de l'envoi du mail, veuillez reessayer")
                            continue
                            
                    else:
                        print("email incorrect veuillez reessayer")
                        continue
            elif mot_de_passe_oublie.lower() == "non":
                print("merci de reessayer")
                break
            else:
                print("veuillez entrer une valeur valide (oui ou non)")
                continue

    while True:
        nouveau_mot_de_passe = input("entrez un nouveau mot de passe :")
        for i in mon_dictionnaire:
            if len(nouveau_mot_de_passe) < 6:
                print("veuillez entrer un mot de passe comportant au moins 6 caracteres")
                continue
            elif nom_utilisateur == i.get("username")  and password == i.get("pass") :
                print("="* 30)
                print("mot de passe deja utilise")
                print("="*30)
                continue
            elif nom_utilisateur == i.get("email") and password != i.get("pass") :
                i["pass"] = nouveau_mot_de_passe
                with open("date_base.json", "w") as f:
                    json.dump(mon_dictionnaire, f, indent=4)
                print("="* 30)
                print(f"mot de passe modifie avec suces \nbienvenue {i.get("username")}")
                print("="*30)
                return True
identification()

