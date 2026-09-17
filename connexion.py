import smtplib
import json
from email.message import EmailMessage
from faker import Faker

fake = Faker(locale="fr_FR")

with open("mail_config.json") as json_file:
    cfg = json.load(json_file)


def sauvegarder(mon_dictionnaire):
    with open("date_base.json", "w") as f:
        json.dump(mon_dictionnaire, f, indent=4)


def envoyer_code(email_destinataire, code):
    """Envoie le code de verification. Retourne True si l'envoi a reussi."""
    msg = EmailMessage()
    msg["to"] = email_destinataire
    msg["from"] = cfg["gmail"]
    msg["subject"] = "mail de verification"
    msg.set_content(f"le code de verification est {code}")
    try:
        with smtplib.SMTP_SSL(cfg["serveur"], cfg["port"]) as smtp:
            smtp.login(cfg["gmail"], cfg["pwd"])
            smtp.send_message(msg)
        print("code envoye")
        return True
    except smtplib.SMTPRecipientsRefused:
        print("email incorrect, veuillez verifier votre email")
        return False
    except smtplib.SMTPException:
        print("une erreur est survenue lors de l'envoi du mail, veuillez reessayer")
        return False


def reinitialiser_mot_de_passe(compte, mon_dictionnaire):
    """compte = le dict (l'entree de mon_dictionnaire) dont on change le mot de passe."""
    while True:
        nouveau_mot_de_passe = input("entrez un nouveau mot de passe :")
        if len(nouveau_mot_de_passe) < 6:
            print("veuillez entrer un mot de passe comportant au moins 6 caracteres")
            continue
        if nouveau_mot_de_passe == compte.get("pass"):
            print("=" * 30)
            print("ce mot de passe est deja utilise, choisissez-en un autre")
            print("=" * 30)
            continue

        compte["pass"] = nouveau_mot_de_passe
        sauvegarder(mon_dictionnaire)
        print("=" * 30)
        print(f"mot de passe modifie avec succes\nbienvenue {compte.get('username')}")
        print("=" * 30)
        return True


def mot_de_passe_oublie_flow(mon_dictionnaire):
    while True:
        reponse = input("avez-vous oublie votre mot de passe ? (oui ou non) :")
        reponse = reponse.lower().strip()

        if reponse == "non":
            print("merci de reessayer")
            return False

        if reponse != "oui":
            print("veuillez entrer une valeur valide (oui ou non)")
            continue

        email = input("entrez votre email :")
        compte = next((i for i in mon_dictionnaire if i.get("email") == email), None)

        if compte is None:
            print("email incorrect veuillez reessayer")
            continue

        code = fake.numerify(text="%%%%%%")
        if not envoyer_code(compte["email"], code):
            continue

        while True:
            saisie = input("veuillez entrer le code a 6 chiffres qui vous est envoye :")
            if saisie == code:
                print("code correct, email valide")
                return reinitialiser_mot_de_passe(compte, mon_dictionnaire)
            print("code incorrect veuillez reessayer")


def identification():
    try:
        with open("date_base.json", "r") as f:
            mon_dictionnaire = json.load(f)
    except FileNotFoundError:
        mon_dictionnaire = []

    while True:
        nom_utilisateur = input("entrez votre nom d'utilisateur ou votre addresse email :")
        password = input("entrez votre mot de passe :")

        compte = next(
            (i for i in mon_dictionnaire
             if nom_utilisateur in (i.get("username"), i.get("email")) and password == i.get("pass")),
            None
        )

        if compte is not None:
            print("=" * 30)
            print(f"bienvenue {compte.get('username')}")
            print("=" * 30)
            return True

        print("nom d'utilisateur ou mot de passe incorrect")
        print("=" * 50)

        ressayer = input("voulez-vous reessayer ? (oui ou non) :")
        ressayer = ressayer.lower().strip()
        if ressayer == "oui":
            continue
        elif ressayer == "non":
            return mot_de_passe_oublie_flow(mon_dictionnaire)
        else:
            print("veuillez entrer une valeur valide (oui ou non)")


if __name__ == "__main__":
    identification()
