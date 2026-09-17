import smtplib
from faker import Faker
import json
from email.message import EmailMessage

fake = Faker(locale="fr_FR")
json_file = open("mail_config.json")
cfg = json.load(json_file)
message = fake.numerify(text="%%%%%%")
msg = EmailMessage()

def inscription():
    try:
        with open("date_base.json", "r") as f:
            mon_dictionnaire = json.load(f)
    except FileNotFoundError:
        mon_dictionnaire = []

    nom = input("quel est votre nom ? :")
    postnom = input("quel est votre postnom ? :")
    prenom = input("quel est votre prenom ? :")

    while True:
        email = input("quel est votre email ? :")
        
        msg["to"] = email
        msg["from"] = cfg["gmail"]
        msg["subject"] = "mail de verification"
        msg.set_content(f"le code de verification est {message}")
        try:
            with smtplib.SMTP_SSL(cfg["serveur"], cfg["port"]) as smtp:
                smtp.login(cfg["gmail"], cfg["pwd"])
                smtp.send_message(msg)
                print("message envoye")
            break
        except smtplib.SMTPRecipientsRefused:
            print("email incorrect, veuillez verifier votre email")
            continue
        except smtplib.SMTPException:
            print("une erreur est survenue lors de l'envoi du mail, veuillez reessayer")
            continue

    while True:
        verification_message = input("veuillez entrer le code a 6 chiffres qui vous est envoye:")
        if verification_message == message :
            print("code correct email valide")
            break
        else:
            print("code incorrect veuillez reessayer")
            continue

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
inscription()



