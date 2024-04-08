"""
Ce module fournit un ensemble de fonctions utilitaires pour l'application IFT-1004 Union,
couvrant diverses fonctionnalités telles que le hachage de mots de passe, la garantie de
l'existence de fichiers nécessaires, la conversion de montants en dollars en centimes,
le formatage de montants monétaires et l'affichage de données sous forme de tableaux.

Fonctions:
- `hacher_mot_de_passe(mot_de_passe)`: Hache un mot de passe en utilisant l'algorithme SHA-256.
- `garantir_existence_fichier(chemin_fichier)`: S'assure qu'un fichier existe; le crée vide le cas échéant.
- `convertir_dollars_vers_centimes(montant_dollars)`: Convertit un montant en dollars en centimes.
- `formater_argent(montant_en_centimes)`: Convertit un montant en centimes en une chaîne formatée en dollars.
- `afficher_tableau(lignes, en_tetes)`: Affiche des données sous forme de tableau dans la console.

Ce module joue un rôle crucial dans la manipulation des données et l'interface utilisateur de l'application,
facilitant la gestion des informations des utilisateurs et des transactions, ainsi que l'amélioration de l'expérience
utilisateur par la présentation claire des informations.

Dépendances:
- `os`: Utilisé pour vérifier l'existence de fichiers et les créer si nécessaire.
- `hashlib`: Nécessaire pour le hachage de mots de passe en utilisant SHA-256.
- `secrets`: Pour comparer les hachages (https://docs.python.org/3/library/secrets.html#secrets.compare_digest).
- `configuration`: Importe des constantes utilisées pour les chemins de fichiers et d'autres paramètres globaux de
l'application.

Note:
    Les fonctions de ce module sont conçues pour être réutilisables et facilement intégrables dans divers points de
    l'application, contribuant à la modularité et à la maintenance du code.
"""

import os
import hashlib
import secrets


def hacher_mot_de_passe(mot_de_passe):
    """Hache un mot de passe en utilisant l'algorithme SHA-256.

    Cette fonction prend un mot de passe en clair comme entrée et retourne
    son hash SHA-256, offrant une forme sécurisée pour stocker ou comparer
    des mots de passe.

    Args:
        mot_de_passe (str): Le mot de passe en clair à hacher.

    Returns:
        str: Le hash SHA-256 du mot de passe.
    """
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()


def garantir_existence_fichier(chemin_fichier):
    """S'assure qu'un fichier existe; le crée vide le cas échéant.

    Cette fonction vérifie si un fichier existe à l'emplacement spécifié par `chemin_fichier`.
    Si le fichier n'existe pas, il est créé vide, permettant ainsi de garantir son existence
    pour les opérations futures.

    Args:
        chemin_fichier (str): Le chemin complet vers le fichier à vérifier ou à créer.
    """
    if not os.path.isfile(chemin_fichier):
        with open(chemin_fichier, "w"):
            pass  # Créer simplement le fichier sans rien écrire


def convertir_dollars_vers_centimes(montant_dollars):
    """Convertit un montant en dollars en centimes.

    Args:
        montant_dollars (float ou int): Le montant en dollars à convertir.

    Returns:
        int: Le montant en centimes.
    """
    return int(montant_dollars * 100)


def formater_argent(montant_en_centimes):
    """Convertit un montant en centimes en une chaîne formatée en dollars.

    Args:
        montant_en_centimes (int): Le montant en centimes à formater.

    Returns:
        str: Le montant formaté en dollars, sous forme de chaîne de caractères,
             avec deux chiffres après le point décimal et des virgules séparant
             les milliers. Suffixé du symbole dollar ($).
    """
    dollars, centimes = divmod(montant_en_centimes, 100)
    return f"{dollars:,.2f} $" if centimes != 0 else f"{dollars:,.0f} $"


def afficher_tableau(lignes, en_tetes):
    """Affiche des données sous forme de tableau dans la console.

    Args:
        lignes (list of list): Une liste de listes, où chaque sous-liste représente les
            données d'une ligne du tableau à afficher.
        en_tetes (list of str): Une liste de chaînes de caractères représentant les
            noms des colonnes du tableau.
    """
    # Trouver la largeur maximale de chaque colonne
    largeurs = [len(max([str(ligne[idx]) for ligne in lignes] + [en_tete], key=len)) for idx, en_tete in
                enumerate(en_tetes)]

    # Créer la ligne d'en-tête
    en_tete_formate = ' | '.join(en_tete.center(largeurs[idx]) for idx, en_tete in enumerate(en_tetes))

    # Créer la ligne de séparation
    ligne_separation = '+-' + '-+-'.join('-' * largeur for largeur in largeurs) + '-+'

    # Afficher l'en-tête
    print(ligne_separation)
    print('| ' + en_tete_formate + ' |')
    print(ligne_separation)

    # Afficher chaque ligne de données
    for ligne in lignes:
        ligne_formatee = ' | '.join(str(item).center(largeurs[idx]) for idx, item in enumerate(ligne))
        print('| ' + ligne_formatee + ' |')

    print(ligne_separation)


