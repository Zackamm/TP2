"""
Ce module est responsable de la gestion des utilisateurs dans l'application IFT-1004 Union,
incluant l'enregistrement de nouveaux utilisateurs et la connexion des utilisateurs existants.
Il interagit avec le fichier des utilisateurs pour enregistrer et vérifier les informations des utilisateurs,
tels que les noms d'utilisateurs, les mots de passe (sous forme hachée), et les soldes initiaux.

Fonctions:
- `enregistrer_utilisateur()`: Enregistre un nouveau utilisateur avec un solde initial.
- `connecter_utilisateur()`: Connecte un utilisateur existant en vérifiant son nom d'utilisateur et son mot de passe.
- `utilisateur_existe(nom_utilisateur)`: Vérifie si un utilisateur existe déjà dans le fichier des utilisateurs.

Ce module utilise `configuration` pour accéder à des constantes globales, `utilitaires` pour des fonctions auxiliaires
comme le hachage de mots de passe, et `transactions` pour enregistrer la transaction initiale lors de la création d'un
nouveau compte utilisateur.

Dépendances:
- `secrets`: Pour comparer les hachages (https://docs.python.org/3/library/secrets.html#secrets.compare_digest).
- `configuration`: Pour accéder à des constantes comme le nom de l'utilisateur admin, le chemin du fichier des
utilisateurs, et le solde initial.
- `utilitaires`: Pour hacher les mots de passe.
- `transactions`: Pour enregistrer la transaction initiale lors de la création d'un nouveau compte.
"""

import secrets
from configuration import NOM_UTILISATEUR_ADMIN, FICHIER_UTILISATEURS, SOLDE_INITIAL
from utilitaires import hacher_mot_de_passe
import transactions


def enregistrer_utilisateur():
    """
    Enregistre un nouvel utilisateur dans le fichier des utilisateurs après avoir effectué
    les vérifications nécessaires.
    
    Demande à l'utilisateur de saisir un nom d'utilisateur et un mot de passe. Vérifie si le nom d'utilisateur existe
    déjà et si le mot de passe est valide (non vide). En cas de succès, enregistre l'utilisateur avec un solde initial
    et enregistre une transaction de ce solde depuis le compte administrateur vers le nouvel utilisateur.
    
    Returns:
        bool: True si l'utilisateur a été enregistré avec succès, sinon False.
    """
    nom_utilisateur = input("Entrez votre nom d'utilisateur : ")
    mot_de_passe = input("Entrez votre mot de passe : ")

    if not nom_utilisateur or not mot_de_passe:
        print("Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
        return False

    if utilisateur_existe(nom_utilisateur):
        print("Ce nom d'utilisateur existe déjà.")
        return False

    hachage_mot_de_passe = hacher_mot_de_passe(mot_de_passe)
    nouveau_utilisateur = f"{nom_utilisateur},{hachage_mot_de_passe},{SOLDE_INITIAL}\n"

    with open(FICHIER_UTILISATEURS, "a") as fichier_utilisateurs:
        fichier_utilisateurs.write(nouveau_utilisateur)

    transactions.enregistrer_transaction(NOM_UTILISATEUR_ADMIN, nom_utilisateur, SOLDE_INITIAL)

    print("Utilisateur enregistré avec succès.")
    return True


def connecter_utilisateur():
    """
    Connecte un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.

    Demande à l'utilisateur de saisir son nom d'utilisateur et son mot de passe. Ces informations sont vérifiées
    contre le fichier des utilisateurs. Si les identifiants sont corrects, l'utilisateur est considéré comme connecté.

    Returns:
        str or None: Le nom d'utilisateur si la connexion est réussie, None sinon.
    """
    nom_utilisateur = input("Nom d'utilisateur : ")
    mot_de_passe = input("Mot de passe : ")

    with open(FICHIER_UTILISATEURS, "r") as fichier_utilisateurs:
        for ligne in fichier_utilisateurs:
            utilisateur, mot_de_passe_hache, _ = ligne.strip().split(",")
            if utilisateur == nom_utilisateur and secrets.compare_digest(hacher_mot_de_passe(mot_de_passe), mot_de_passe_hache):
                print("Connecté avec succès.")
                return nom_utilisateur

    print("Nom d'utilisateur ou mot de passe incorrect.")
    return None


def utilisateur_existe(nom_utilisateur):
    """Vérifie si un nom d'utilisateur existe déjà dans le fichier des utilisateurs.

    Cette fonction parcourt le fichier des utilisateurs, ligne par ligne, pour rechercher un nom d'utilisateur
    spécifique. Si le nom d'utilisateur est trouvé dans le fichier, la fonction retourne True,
    sinon False.

    Args:
        nom_utilisateur (str): Le nom d'utilisateur à rechercher.

    Returns:
        bool: True si le nom d'utilisateur est trouvé, sinon False.
    """
    with open(FICHIER_UTILISATEURS, "r") as fichier_utilisateurs:
        for ligne in fichier_utilisateurs:
            utilisateur, _, _ = ligne.strip().split(",")
            if utilisateur == nom_utilisateur:
                return True
    return False
