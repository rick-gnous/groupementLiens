from flask import Flask, render_template, request, redirect, url_for, make_response
from os import path
from bs4 import BeautifulSoup

app = Flask('ui', static_url_path="/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def slash():
    response = make_response(render_template("index.html"))
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.route("/ajout")
def ajout():
    return render_template("ajout.html")

@app.route("/apropos")
def apropos():
    return render_template("apropos.html")

@app.route("/bizutage", methods=["POST"])
def bizutage():
    if request.method == "POST":
        titre = request.values['titre'] 
        lien = request.values['lien'] 
        desc = request.values['desc'] 
        nouvLien = "<div class=\"elem\"><h2>{}</h2><p><a href=\"{}\">Lien</a></p><hr><p>{}</p>".format(titre, lien, desc)
        nouvLienHtml = BeautifulSoup(nouvLien, "html.parser")

        if nouvLienHtml.find("script") != None:
            erreur = "Vous ne pouvez pas charger de balises script !"
            return render_template("ajout.html", erreur=erreur)

        with open("templates/index.html", 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            soup.find("hr").insert_after("", nouvLienHtml)
        with open("templates/index.html", 'w') as file:
            file.write(soup.prettify())

        with open("lite/index.html", 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            soup.find("hr").insert_after("", nouvLienHtml)
        with open("lite/index.html", 'w') as file:
            file.write(soup.prettify())

        reussite = "Lien ajouté !"
    else:
        print("error")
    return render_template("ajout.html", reussi=reussite)

if __name__ == "__main__":
    app.run()
