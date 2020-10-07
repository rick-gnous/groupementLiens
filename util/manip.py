import re
import json
from util.status import Status

class Manip():
    def __init__(self, cheminFichier: str):
        self.fichierJson = cheminFichier

    def ajoutLienJson(self, infoLiens) -> Status:
        """
        Insère dans le fichier json le nouveau lien

        :param infoLiens dic: dictionnaire avec le lien qui sera 
         inséré dans le fichier json. Le dictionnaire doit contenir
         toutes les informations !

        :rtype Status: le status de l’instertion (réussie, échouée…)
        """
        ret = Status.ERREUR_LIEN
        if self.valideUrl(infoLiens["url"]):
            try:
                with open(self.fichierJson, "r+") as file:
                    temp = json.load(file)
                    temp["liens"].append(infoLiens)
                    file.seek(0)
                    json.dump(temp, file, indent=4)
                ret = Status.BON
            except Exception as err:
                ret = Status.ERREUR_INSERTION
                #TODO ajouté logging pour retrouer l’erreur
        return ret

    def valideUrl(self, url: str) -> bool:
        """
        Vérifie si une url est valide

        :param url str: l’url à vérifier
        :rtype bool: true si l’url est bonne
                     false sinon
        """
        # thx django
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return bool(re.search(regex, url))
