"""
Ce module gère les opérations de transaction dans l'application IFT-1004 Union,
telles que l'envoi d'argent entre utilisateurs, la consultation du solde et l'historique des transactions.
Il offre des fonctionnalités clés pour interagir avec les données des utilisateurs et des transactions stockées
dans des fichiers.

Fonctions:
- `envoyer_argent(nom_utilisateur)`: Permet à un utilisateur d'envoyer de l'argent à un autre utilisateur,
  en appliquant des frais de transaction et en mettant à jour les soldes des comptes concernés.
- `recuperer_solde(nom_utilisateur)`: Récupère le solde actuel d'un utilisateur.
- `consulter_solde(nom_utilisateur)`: Affiche le solde actuel d'un utilisateur.
- `consulter_transactions(nom_utilisateur)`: Affiche l'historique des transactions d'un utilisateur.
- `ajouter_au_solde(nom_utilisateur, montant)`: Met à jour le solde d'un utilisateur suite à une transaction.
- `enregistrer_transaction(expediteur, destinataire, montant, frais=0)`: Enregistre une transaction dans le fichier des
transactions.
- `calculer_frais(montant)`: Calcule les frais de transaction basés sur le montant envoyé.

Ce module interagit directement avec `configuration` pour accéder à des constantes de configuration,
avec `utilitaires` pour des opérations telles que l'affichage des tableaux ou le formatage des montants,
et lit/mise à jour les fichiers `FICHIER_UTILISATEURS` et `FICHIER_TRANSACTIONS` pour gérer les données.

Dépendances:
- `os`: Pour la gestion des fichiers.
- `datetime`: Pour enregistrer la date et l'heure des transactions.
- `configuration`: Pour accéder aux chemins des fichiers et aux configurations des frais de transaction.
- `utilitaires`: Pour des fonctions auxiliaires comme l'affichage de tableaux formatés, la conversion de montants en
 dollars vers les centimes, le formatage de montants en dollars.
- `gestion_utilisateurs`: Pour vérifier l'existence d'un utilisateur dans le système.
"""

import os
from datetime import datetime
from configuration import FICHIER_UTILISATEURS, FICHIER_TRANSACTIONS, FRAIS_TRANSACTIONS
from utilitaires import afficher_tableau, convertir_dollars_vers_centimes, formater_argent
import gestion_utilisateurs


def envoyer_argent(nom_utilisateur):
    """
    Permet à un utilisateur d'envoyer de l'argent à un autre utilisateur en prenant en compte des frais de transaction.

    Args:
        nom_utilisateur (str): Le nom de l'utilisateur qui envoie l'argent.

    Returns:
        bool: True si la transaction a été effectuée avec succès, False en cas d'échec.
    
    L'utilisateur est invité à entrer le nom du destinataire et le montant en dollars à envoyer. La fonction vérifie
    que le destinataire existe, que l'utilisateur ne s'envoie pas de l'argent à lui-même, et que le montant est positif.
    Les frais de transaction sont calculés et ajoutés au montant à envoyer. La fonction vérifie ensuite si l'utilisateur
    dispose de suffisamment de fonds. Si c'est le cas, le montant (plus les frais) est débité du compte de l'expéditeur
    et crédité au destinataire.
    """
    destinataire = input("Entrez le nom du destinataire : ")
    montant_dollars = float(input("Entrez le montant à envoyer en dollars : "))

    if destinataire == nom_utilisateur:
        print("Vous ne pouvez pas vous envoyer de l'argent à vous-même.")
        return False

    if montant_dollars <= 0:
        print("Le montant doit être positif.")
        return False

    solde_exp = recuperer_solde(nom_utilisateur)
    montant_centimes = convertir_dollars_vers_centimes(montant_dollars)
    frais = calculer_frais(montant_centimes)

    if solde_exp < montant_centimes + frais:
        print("Fonds insuffisants.")
        return False

    solde_dest = recuperer_solde(destinataire)

    if not ajouter_au_solde(nom_utilisateur, -montant_centimes - frais) or \
            not ajouter_au_solde(destinataire, montant_centimes):
        print("Une erreur s'est produite lors de la transaction.")
        return False

    enregistrer_transaction(nom_utilisateur, destinataire, montant_centimes, frais)

    print("Transaction effectuée avec succès.")
    return True


def recuperer_solde(nom_utilisateur):
    """
    Récupère le solde actuel d'un utilisateur.

    Args:
        nom_utilisateur (str): Le nom de l'utilisateur dont on souhaite consulter le solde.

    Returns:
        int: Le solde de l'utilisateur en centimes.

    Cette fonction lit le fichier des utilisateurs et retourne le solde en centimes du nom d'utilisateur spécifié.
    """
    with open(FICHIER_UTILISATEURS, "r") as fichier:
        for ligne in fichier:
            utilisateur, _, solde = ligne.strip().split(",")
            if utilisateur == nom_utilisateur:
                return int(solde)
    return 0


def consulter_solde(nom_utilisateur):
    """
    Affiche le solde actuel de l'utilisateur.

    Args:
        nom_utilisateur (str): Le nom de l'utilisateur dont on souhaite consulter le solde.

    Cette fonction récupère le solde de l'utilisateur (grâce à la fonction `recuperer_solde`) et l'affiche de
    manière formatée (grâce à la fonction utilitaire `formater_argent`).
    """
    solde = recuperer_solde(nom_utilisateur)
    solde_formatte = formater_argent(solde)
    print(f"Solde actuel de {nom_utilisateur} : {solde_formatte}")


def consulter_transactions(nom_utilisateur):
    """
    Affiche toutes les transactions impliquant l'utilisateur spécifié.

    Args:
        nom_utilisateur (str): Le nom de l'utilisateur pour lequel afficher les transactions.

    Cette fonction parcourt le fichier des transactions et affiche toutes les transactions où l'utilisateur
    spécifié est l'expéditeur ou le destinataire. Les transactions sont affichées dans un tableau formaté (grâce à la
    fonction utilitaire `afficher_tableau`).
    """
    transactions_utilisateur = []

    with open(FICHIER_TRANSACTIONS, "r") as fichier_transactions:
        for ligne in fichier_transactions:
            expediteur, destinataire, montant, frais, date_heure = ligne.strip().split(",")
            if expediteur == nom_utilisateur or destinataire == nom_utilisateur:
                montant_formatte = formater_argent(int(montant))
                frais_formatte = formater_argent(int(frais))
                transactions_utilisateur.append([date_heure, expediteur, destinataire, montant_formatte, frais_formatte])

    if transactions_utilisateur:
        afficher_tableau(transactions_utilisateur, ["Date/Heure", "Expéditeur", "Destinataire", "Montant", "Frais"])
    else:
        print("Aucune transaction trouvée pour cet utilisateur.")


def ajouter_au_solde(nom_utilisateur, montant):
    """
    Ajoute un montant spécifié au solde de l'utilisateur.

    Args:
        nom_utilisateur (str): Le nom de l'utilisateur pour lequel mettre à jour le solde.
        montant (int): Le montant à ajouter (positif ou négatif).

    Returns:
        bool: True si la mise à jour du solde a réussi, False sinon.

    Cette fonction lit le fichier des utilisateurs, met à jour le solde de l'utilisateur spécifié avec le montant
    donné, et réécrit le fichier avec le nouveau solde. Elle retourne True si l'opération s'est déroulée avec succès,
    sinon False.
    """
    lignes_utilisateurs = []

    with open(FICHIER_UTILISATEURS, "r") as fichier_utilisateurs:
        for ligne in fichier_utilisateurs:
            utilisateur, mot_de_passe, solde = ligne.strip().split(",")
            if utilisateur == nom_utilisateur:
                solde = str(int(solde) + montant)
            lignes_utilisateurs.append(f"{utilisateur},{mot_de_passe},{solde}\n")

    with open(FICHIER_UTILISATEURS, "w") as fichier_utilisateurs:
        fichier_utilisateurs.writelines(lignes_utilisateurs)

    return True


def enregistrer_transaction(expediteur, destinataire, montant, frais=0):
    """
    Enregistre une transaction dans le fichier des transactions.

    Args:
        expediteur (str): Le nom de l'utilisateur expéditeur.
        destinataire (str): Le nom de l'utilisateur destinataire.
        montant (int): Le montant de la transaction en centimes.
        frais (int): Les frais de transaction en centimes (par défaut à 0).

    Cette fonction enregistre une transaction dans le fichier des transactions en y ajoutant une nouvelle ligne
    contenant les informations sur l'expéditeur, le destinataire, le montant, les frais et la date/heure de la
    transaction.
    """
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nouvelle_transaction = f"{expediteur},{destinataire},{montant},{frais},{date_heure}\n"

    with open(FICHIER_TRANSACTIONS, "a") as fichier_transactions:
        fichier_transactions.write(nouvelle_transaction)


def calculer_frais(montant):
    """
    Calcule les frais de transaction en fonction du montant envoyé.

    Args:
        montant (int): Le montant de la transaction en centimes.

    Returns:
        int: Les frais de transaction en centimes.

    Cette fonction calcule les frais de transaction en fonction de la structure définie dans le fichier de configuration.
    """
    from configuration import FRAIS_TRANSACTIONS

    for tranche in FRAIS_TRANSACTIONS:
        if tranche["min"] <= montant <= tranche["max"]:
            return int(montant * tranche["frais"] / 100)
    return 0
