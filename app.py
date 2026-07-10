from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

# --- Connexion DB ---
DATABASE = "ufrsta.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# --- Pages publiques ---
@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/departements")
def departements():
    return render_template("departements.html")

@app.route("/actualites")
def actualites():
    return render_template("actualites.html")

@app.route("/activites")
def activites():
    return render_template("activites.html")

@app.route("/galerie")
def galerie():
    return render_template("galerie.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        sujet = request.form.get('sujet')
        message = request.form.get('message')
        return "Message reçu, merci !"
    return render_template("contact.html")

@app.route("/enseignants")
def enseignants():
    return render_template("enseignants.html")

@app.route("/formations")
def formations():
    return render_template("formations.html")

# --- Admin Dashboard ---
@app.route("/admin")
def admin():
    return render_template("admin/dashboard.html")

# --- Gestion des formations ---
@app.route("/admin/formations")
def gerer_formations():
    return render_template("admin/gerer_formations.html")

# --- Gestion des actualités ---
@app.route("/admin/actualites")
def gerer_actualites():
    db = get_db()
    actualites = db.execute("SELECT * FROM actualites").fetchall()
    return render_template("admin/gerer_actualites.html", actualites=actualites)

@app.route("/admin/actualites/ajouter", methods=['POST'])
def ajouter_actualite():
    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]
    photo = request.form.get("photo")

    db = get_db()
    db.execute(
        "INSERT INTO actualites (titre, date, description, photo) VALUES (?, ?, ?, ?)",
        (titre, date, description, photo)
    )
    db.commit()
    return redirect(url_for("gerer_actualites"))

# --- Gestion des photos ---
@app.route("/admin/photos/ajouter", methods=["POST"])
def ajouter_photo():
    titre = request.form["titre"]
    lien = request.form["lien"]

    db = get_db()
    db.execute(
        "INSERT INTO photos (titre, lien) VALUES (?, ?)",
        (titre, lien)
    )
    db.commit()
    return redirect(url_for("gerer_photos"))

@app.route("/admin/photos/modifier/<int:id>", methods=["POST"])
def modifier_photo(id):
    titre = request.form["titre"]
    lien = request.form["lien"]

    db = get_db()
    db.execute(
        "UPDATE photos SET titre=?, lien=? WHERE id=?",
        (titre, lien, id)
    )
    db.commit()
    return redirect(url_for("gerer_photos"))

@app.route("/admin/photos/supprimer/<int:id>", methods=["POST"])
def supprimer_photo(id):
    db = get_db()
    db.execute("DELETE FROM photos WHERE id=?", (id,))
    db.commit()
    return redirect(url_for("gerer_photos"))

@app.route("/admin/actualites/modifier/<int:id>", methods=["POST"])
def modifier_actualite(id):
    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]
    photo = request.form.get("photo")

    db = get_db()
    db.execute(
        "UPDATE actualites SET titre=?, date=?, description=?, photo=? WHERE id=?",
        (titre, date, description, photo, id)
    )
    db.commit()
    return redirect(url_for("gerer_actualites"))

@app.route("/admin/actualites/supprimer/<int:id>", methods=["POST"])
def supprimer_actualite(id):
    db = get_db()
    db.execute("DELETE FROM actualites WHERE id=?", (id,))
    db.commit()
    return redirect(url_for("gerer_actualites"))



# --- Gestion des activités ---
@app.route("/admin/activites")
def gerer_activites():
    db = get_db()
    activites = db.execute("SELECT * FROM activites").fetchall()
    return render_template("admin/gerer_activites.html", activites=activites)


@app.route("/admin/activites/ajouter", methods=["POST"])
@app.route("/admin/activites/ajouter", methods=["POST"])
@app.route("/admin/activites/ajouter", methods=["POST"])
def ajouter_activite():
    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]
    lieu = request.form["lieu"]
    organisateur = request.form["organisateur"]

    db = get_db()
    db.execute(
        "INSERT INTO activites (titre, date, description, lieu, organisateur) VALUES (?, ?, ?, ?, ?)",
        (titre, date, description, lieu, organisateur)
    )
    db.commit()
    return redirect(url_for("gerer_activites"))


    

   

@app.route("/admin/activites/modifier/<int:id>", methods=["POST"])
def modifier_activite(id):
    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]

    db = get_db()
    db.execute(
        "UPDATE activites SET titre=?, date=?, description=? WHERE id=?",
        (titre, date, description, id)
    )
    db.commit()
    return redirect(url_for("gerer_activites"))

@app.route("/admin/activites/supprimer/<int:id>", methods=["POST"])
def supprimer_activite(id):
    db = get_db()
    db.execute("DELETE FROM activites WHERE id=?", (id,))
    db.commit()
    return redirect(url_for("gerer_activites"))


# --- Gestion de la galerie ---
@app.route("/admin/galerie")
def gerer_photos():
    return render_template("admin/gerer_photos.html")

# --- Gestion des départements ---
@app.route("/admin/departements")
def gerer_departements():
    return render_template("admin/gerer_departements.html")

# --- Login ---
@app.route("/admin/login")
def login():
    return render_template("admin/login.html")

if __name__ == "__main__":
    app.run(debug=True)
