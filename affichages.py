"""
Module d'affichage pour l'application IFT-1004 Union.

Ce module fournit des fonctions d'affichage réutilisables pour l'application IFT-1004 Union.
Il est conçu pour centraliser toutes les fonctions liées à l'affichage dans la console,
y compris l'affichage des bannières, des menus principaux et des menus utilisateurs.

Fonctions:
    afficher_banniere(titre): Affiche une bannière contenant un titre centré.
    afficher_menu_principal(): Affiche le menu principal de l'application.
    afficher_menu_utilisateur(): Affiche le menu destiné aux utilisateurs connectés.
"""


def afficher_banniere(titre):
    """Affiche une bannière contenant un titre centré.

    Args:
        titre (str): Le titre à afficher au centre de la bannière.
    """
    largeur_banniere = len(titre) + 20
    print(largeur_banniere * "#")
    print(f"{titre:^{largeur_banniere}}")
    print(largeur_banniere * "#")


def afficher_menu_principal():
    """Affiche le menu principal de l'application.

    Cette fonction affiche un menu permettant à l'utilisateur de choisir parmi
    les options de création de compte, de connexion ou de quitter l'application.
    """
    print("\nMenu Principal")
    print("1. Créer un compte")
    print("2. Se connecter")
    print("3. Quitter\n")


def afficher_menu_utilisateur():
    """Affiche le menu utilisateur de l'application.

    Cette fonction affiche un menu destiné aux utilisateurs
    connectés. Il leur permet de choisir parmi les options d'envoi d'argent,
    de consultation de solde, de transactions ou de déconnexion.
    """
    print("\nMenu Utilisateur")
    print("1. Envoyer de l'argent")
    print("2. Consulter mon solde")
    print("3. Consulter mes transactions")
    print("4. Se déconnecter\n")
