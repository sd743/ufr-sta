from flask import Flask, render_template, request, redirect, g, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"


# ============================================================
# PAGES PUBLIQUES (visiteurs)
# ============================================================
@app.route("/accueil")
def accueil():
    return render_template("index.html")


@app.route("/activites")
def activites():
    return render_template("activites.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/gallerie")
def gallery():
    return render_template("gallerie.html")


@app.route("/actualites")
def actualites():
    return render_template("actualites.html")


@app.route("/departements")
def departements():
    return render_template("departements.html")


@app.route("/formations")
def formations():
    return render_template("formations.html")

# ============================================================
# CONNEXION À LA BASE DE DONNÉES
# ============================================================
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # permet d'accéder aux colonnes par nom (ex: actu["titre"])
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# ===========================
# PAGE DE CONNEXION
# ===========================
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM administrateurs WHERE email=? AND mot_de_passe=?",
            (email, password)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin:
            return redirect(url_for("dashboard"))
        else:
            return "Email ou mot de passe incorrect"

    return render_template("admin/login.html")

# ============================================================
# ADMINISTRATION - DASHBOARD ET LOGIN
# ============================================================
@app.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

# ============================================================
# ADMINISTRATION - GESTION DES ACTUALITÉS (CRUD complet)
# ============================================================

# ---------- LISTER (READ) ----------
@app.route('/admin/gerer_actualites')
def gerer_actualites():
    db = get_db()
    liste_actualites = db.execute("SELECT * FROM actualites ORDER BY date DESC").fetchall()
    return render_template('admin/gerer_actualites.html', actualites=liste_actualites)


# ---------- AJOUTER (CREATE) ----------
@app.route('/admin/actualites/ajouter', methods=['POST'])
def ajouter_actualite():
    titre = request.form['titre']
    date = request.form['date']
    description = request.form['description']
    photo = request.form.get('photo')  # champ optionnel

    db = get_db()
    db.execute(
        "INSERT INTO actualites (titre, date, description, photo) VALUES (?, ?, ?, ?)",
        (titre, date, description, photo)
    )
    db.commit()
    return redirect(url_for('gerer_actualites'))


# ---------- MODIFIER : afficher le formulaire pré-rempli (READ) ----------
@app.route('/admin/actualites/modifier/<int:id>', methods=['GET'])
def modifier_actualite_form(id):
    db = get_db()
    actualite = db.execute("SELECT * FROM actualites WHERE id=?", (id,)).fetchone()
    return render_template('admin/modifier_actualite.html', actualite=actualite)


# ---------- MODIFIER : enregistrer les changements (UPDATE) ----------
@app.route('/admin/actualites/modifier/<int:id>', methods=['POST'])
def modifier_actualite(id):
    titre = request.form['titre']
    date = request.form['date']
    description = request.form['description']
    photo = request.form.get('photo')

    db = get_db()
    db.execute(
        "UPDATE actualites SET titre=?, date=?, description=?, photo=? WHERE id=?",
        (titre, date, description, photo, id)
    )
    db.commit()
    return redirect(url_for('gerer_actualites'))


# ---------- SUPPRIMER (DELETE) ----------
@app.route('/admin/actualites/supprimer/<int:id>', methods=['POST'])
def supprimer_actualite(id):
    db = get_db()
    db.execute("DELETE FROM actualites WHERE id=?", (id,))
    db.commit()
    return redirect(url_for('gerer_actualites'))


# ============================================================
# ADMINISTRATION - ACTIVITÉS, FORMATIONS, PHOTOS
# (pour l'instant en lecture seule - à compléter avec le même
#  pattern que les actualités ci-dessus : ajouter/modifier/supprimer)
# ============================================================
@app.route('/admin/gerer_activites')
def gerer_activites():
    db = get_db()
    liste_activites = db.execute("SELECT * FROM activites ORDER BY date DESC").fetchall()
    return render_template('admin/gerer_activites.html', activites=liste_activites)


@app.route('/admin/gerer_formations')
def gerer_formations():
    db = get_db()
    liste_formations = db.execute("SELECT * FROM formations").fetchall()
    return render_template('admin/gerer_formations.html', formations=liste_formations)


@app.route('/admin/gerer_photos')
def gerer_photos():
    db = get_db()
    liste_photos = db.execute("SELECT * FROM galerie").fetchall()
    return render_template('admin/gerer_photos.html', photos=liste_photos)


if __name__ == "__main__":
    app.run(debug=True, port=5000)