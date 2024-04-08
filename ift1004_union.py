"""
Point d'entrée principal pour l'application IFT-1004 Union.

Ce module coordonne le déroulement général de l'application, de la vérification de l'existence des fichiers nécessaires,
à l'affichage des menus et la gestion de l'interaction avec l'utilisateur.

Les utilisateurs peuvent créer un compte, se connecter, effectuer des transactions, consulter leur solde,
leurs transactions, ou se déconnecter. Les interactions sont gérées à travers une boucle principale
qui sollicite l'action de l'utilisateur et appelle les fonctions appropriées en réponse.

Fonctions:
- main(): Lance l'application, gérant le flux principal et les interactions utilisateur.

Ce module fait usage des configurations définies dans `configuration.py` et utilise des fonctions définies dans
d'autres modules comme `affichages`, `utilitaires`, `gestion_utilisateurs`, et `transactions` pour accomplir ses tâches.
"""

from affichages import afficher_banniere, afficher_menu_principal, afficher_menu_utilisateur
from configuration import FICHIER_UTILISATEURS, FICHIER_TRANSACTIONS
from utilitaires import garantir_existence_fichier
from gestion_utilisateurs import enregistrer_utilisateur, connecter_utilisateur
from transactions import envoyer_argent, consulter_solde, consulter_transactions


def main():
    """Fonction principale de l'application IFT-1004 Union.

    Cette fonction lance l'application, s'assurant de l'existence des fichiers nécessaires,
    affiche une bannière de bienvenue et gère le flux principal de l'application, y compris
    l'affichage des menus et la gestion des actions des utilisateurs. L'utilisateur peut choisir
    de créer un compte, se connecter avec un compte existant, ou quitter l'application. Une fois
    connecté, l'utilisateur a accès à des actions supplémentaires telles qu'envoyer de l'argent,
    consulter son solde, consulter ses transactions, ou se déconnecter.

    La boucle principale gère la navigation entre le menu principal et le menu utilisateur,
    traitant les entrées de l'utilisateur et exécutant les actions correspondantes.
    """
    garantir_existence_fichier(FICHIER_UTILISATEURS)
    garantir_existence_fichier(FICHIER_TRANSACTIONS)

    afficher_banniere("Bienvenue sur IFT-1004 Union !")

    continuer = True
    while continuer:
        afficher_menu_principal()
        action = int(input("Choisissez une action: "))
        if action == 1:
            enregistrer_utilisateur()
        elif action == 2:
            nom_utilisateur = connecter_utilisateur()
            if nom_utilisateur:
                connecte = True
                while connecte:
                    afficher_menu_utilisateur()
                    action_utilisateur = int(input("Choisissez une action: "))
                    if action_utilisateur == 1:
                        envoyer_argent(nom_utilisateur)
                    elif action_utilisateur == 2:
                        consulter_solde(nom_utilisateur)
                    elif action_utilisateur == 3:
                        consulter_transactions(nom_utilisateur)
                    elif action_utilisateur == 4:
                        connecte = False
                    else:
                        print("Action utilisateur invalide.")
        elif action == 3:
            continuer = False
        else:
            print("Action invalide.")


if __name__ == "__main__":
    main()
