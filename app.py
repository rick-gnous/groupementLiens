from flask import Flask, render_template, request, redirect, url_for, make_response, Markup
from enum import Enum
from bs4 import BeautifulSoup

app = Flask('ui', static_url_path="/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Status(Enum):
    ERREUR_LIEN = "Le lien doit être en http ou https !",
    BON = "Lien ajouté !"

def ecritureFichierHtml(nouvLien, cheminFichier):
    with open(cheminFichier, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        soup.find("hr").insert_after("", nouvLien)
    with open(cheminFichier, 'w') as file:
        file.write(soup.prettify())

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

@app.route("/bizutage", methods=["POST"])
def bizutage():
    if request.method == "POST":
        lien = request.values['lien'] 
        if not (lien.startswith("http") or lien.startswith("https")):
            return render_template("ajout.html", erreur=Status.ERREUR_LIEN.value)

        titre = Markup.escape(request.values['titre'])
        desc = Markup.escape(request.values['desc'])
        nouvLien = "<div class=\"elem\"><h2>{}</h2><p><a href=\"{}\">Lien</a></p><hr><p>{}</p>".format(titre, lien, desc)
        nouvLienHtml = BeautifulSoup(nouvLien, "html.parser")

        ecritureFichierHtml(nouvLienHtml, "static/index.html")
        ecritureFichierHtml(nouvLienHtml, "lite/index.html")

    else:
        print("error")
    return render_template("ajout.html", reussi=Status.BON.value)

if __name__ == "__main__":
    app.run()
