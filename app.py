from flask import Flask, render_template, request, redirect, make_response, \
    Markup
from bs4 import BeautifulSoup
import json
from util.status import Status
from util.manip import Manip
#from util.genHtml import GenerationHtml

__author__ = "rick@gnous.eu | Romain"
__licence__ = "GPL3 or later"

app = Flask('ui', static_url_path="/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

fichierJson = "listeLiens.json"
listeCategorie = ["autres", "informatique", "musique"]

manip = Manip(fichierJson)
#generateurHml = GenerationHtml(fichierJson, listeCategorie)

@app.route('/')
def slash():
    with open(fichierJson, 'r') as fichier:
        liens = json.load(fichier)
    listeLiens = liens["liens"]
    listeLiens.reverse()
    response = make_response(render_template("index.html", listeLiens=listeLiens))
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.route("/categories/<path:subpath>")
def categories(subpath):
    if subpath in listeCategorie:
        listeLiensCategorie = []
        with open(fichierJson, 'r') as fichierLiens:
            listeLiens = json.load(fichierLiens)
            for lien in listeLiens["liens"]:
                if lien["categorie"] == subpath:
                    listeLiensCategorie.append(lien)
        listeLiensCategorie.reverse()
        return render_template("index.html", listeLiens=listeLiensCategorie)

@app.route("/ajout")
def ajout():
    return render_template("ajout.html")

@app.route("/recherche")
def recherche():
    with open(fichierJson, 'r') as fichier:
        liens = json.load(fichier)
    listeLiens = liens["liens"]
    listeLiens.reverse()
    response = make_response(render_template("recherche.html", listeLiens=listeLiens))
    return response

@app.route("/apropos")
def apropos():
    return app.send_static_file("apropos.html")

@app.route("/bizutage", methods=["GET"])
def bizutage_redirect():
    return redirect('/')

@app.route("/bizutage", methods=["POST"])
def bizutage():
    lien = request.values["lien"] 

    titre = Markup.escape(request.values["titre"])
    desc = Markup.escape(request.values["desc"])
    categorie = Markup.escape(request.values["categories"])
    tagsList = request.values["tags"].split(';')
    tags = []
    for i in tagsList:
        i.strip()
        i = Markup.escape(i)
        if i not in tags:
            tags.append(i)

    nouvLien = {"titre": titre,
                "url": lien,
                "desc": desc,
                "categorie": categorie,
                "tags": tags
               }

    ret = manip.ajoutLienJson(nouvLien)
    if ret is Status.BON:
        #generateurHml.majTousFichiers()
        return render_template("ajout.html", reussi=ret.value)
    else:
        return render_template("ajout.html", erreur=ret.value)

if __name__ == "__main__":
    app.run()
