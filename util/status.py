from enum import Enum

class Status(Enum):
    ERREUR_LIEN = "Le lien doit être en http/s et valide !"
    ERREUR_INSERTION = "Une erreur a été rencontrée lors de l’insertion."
    ERREUR_INCONNUE = "Une erreur inconnue a été rencontrée."
    BON = "Lien ajouté succés !"
