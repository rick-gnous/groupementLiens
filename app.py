from flask import Flask, render_template, request, redirect, make_response, \
    Markup
from enum import Enum
from bs4 import BeautifulSoup
import re

__author__ = "rick@gnous.eu | Romain"
__licence__ = "GPL3 or later"

app = Flask('ui', static_url_path="/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Status(Enum):
    ERREUR_LIEN = "Le lien doit être en http ou https et valide !"
    ERREUR_INCONNUE = "Une erreur inconnue a été rencontrée !"
    BON = "Lien ajouté !"

class Manip():
    def ecritureFichierHtml(nouvLien, cheminFichier):
        nouvLienHtml = BeautifulSoup(nouvLien, "html.parser")
        with open(cheminFichier, 'r+') as file:
            soup = BeautifulSoup(file, 'html.parser')
            soup.find("hr").insert_after("", nouvLienHtml)
            file.seek(0)
            file.write(soup.prettify())
    
    def valideUrl(url: str) -> bool:
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

@app.route('/')
def slash():
    response = make_response(app.send_static_file("index.html"))
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.route("/categories/<path:subpath>")
def categories(subpath):
    return app.send_static_file(subpath + ".html")

@app.route("/ajout")
def ajout():
    return render_template("ajout.html")

@app.route("/apropos")
def apropos():
    return app.send_static_file("apropos.html")

@app.route("/bizutage", methods=["GET"])
def bizutage_redirect():
    return redirect('/')

@app.route("/bizutage", methods=["POST"])
def bizutage():
    lien = request.values["lien"] 
    if not Manip.valideUrl(lien):
        return render_template(
            "ajout.html", 
            erreur=Status.ERREUR_LIEN.value
        )

    titre = Markup.escape(request.values["titre"])
    desc = Markup.escape(request.values["desc"])
    categorie = Markup.escape(request.values["categories"])
    nouvLien = f"""<div class="elem {categorie}">
                      <h2>{titre}</h2>
                      <p><a href=\"{lien}\">{lien}</a></p>
                      <hr>
                      <p>{desc}</p>
                   </div>"""

    Manip.ecritureFichierHtml(nouvLien, "static/index.html")
    Manip.ecritureFichierHtml(nouvLien, "static/" + categorie + ".html")
    Manip.ecritureFichierHtml(nouvLien, "lite/index.html")
    Manip.ecritureFichierHtml(nouvLien, "lite/" + categorie + ".html")
    return render_template("ajout.html", reussi=Status.BON.value)

if __name__ == "__main__":
    app.run()
