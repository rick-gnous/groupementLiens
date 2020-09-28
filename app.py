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
    BON = "Lien ajouté !"

def ecritureFichierHtml(nouvLien, cheminFichier):
    with open(cheminFichier, 'r+') as file:
        soup = BeautifulSoup(file, 'html.parser')
        soup.find("hr").insert_after("", nouvLien)
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
    if request.method == "POST":
        lien = request.values['lien'] 
        if not valideUrl(lien):
            return render_template(
                "ajout.html", 
                erreur=Status.ERREUR_LIEN.value
            )

        titre = Markup.escape(request.values['titre'])
        desc = Markup.escape(request.values['desc'])
        nouvLien = f"""<div class="elem">
                          <h2>{titre}</h2>
                          <p><a href=\"{lien}\">Lien</a></p>
                          <hr>
                          <p>{desc}</p>
                       </div>"""
        nouvLienHtml = BeautifulSoup(nouvLien, "html.parser")

        ecritureFichierHtml(nouvLienHtml, "static/index.html")
        ecritureFichierHtml(nouvLienHtml, "lite/index.html")

    else:
        print("error")
    return render_template("ajout.html", reussi=Status.BON.value)

if __name__ == "__main__":
    app.run()
