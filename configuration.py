"""
Configuration pour l'application IFT-1004 Union.

Ce module définit plusieurs constantes utilisées à travers l'application.
Cela inclut les chemins vers les fichiers nécessaires, les paramètres par défaut
comme le solde initial pour les nouveaux comptes, et d'autres valeurs configurables
comme les frais de transaction.
"""

import math
from pathlib import Path
from utilitaires import convertir_dollars_vers_centimes


# Définit le dossier de base de l'application comme étant le dossier contenant ce fichier de configuration.
DOSSIER_BASE = Path(__file__).resolve().parent

# Chemin vers le fichier stockant les informations des utilisateurs.
FICHIER_UTILISATEURS = DOSSIER_BASE / "utilisateurs.txt"

# Chemin vers le fichier stockant les transactions entre utilisateurs.
FICHIER_TRANSACTIONS = DOSSIER_BASE / "transactions.txt"

# Solde initial en centimes attribué à chaque nouvel utilisateur.
SOLDE_INITIAL = convertir_dollars_vers_centimes(1000)

# Nom d'utilisateur pour le compte administrateur de l'application.
NOM_UTILISATEUR_ADMIN = "ift-1004-union"

# Structure définissant les frais de transaction en fonction du montant transféré, en dollars.
# N'oubliez pas : en programmation, la seule vraie taxe, c'est l'imagination (et les frais de transactions apparemment).
FRAIS_TRANSACTIONS = [
    {"min": 0, "max": 100, "frais": 5},
    {"min": 101, "max": 500, "frais": 10},
    {"min": 501, "max": 1000, "frais": 15},
    {"min": 1001, "max": 5000, "frais": 20},
    {"min": 5001, "max": math.inf, "frais": 25},
]
