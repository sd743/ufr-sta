from flask import Flask, render_template, request, redirect, g, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "database/database.db"


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

@app.route("/enseignants")
def enseignants():
    return render_template("enseignants.html")

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

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

conn.close()

# ===========================
# PAGE DE CONNEXION
# ===========================
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM administrateurs WHERE email=? AND mot_de_passe=?",
            (email, password)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin:
            return redirect(url_for ("admin_dashboard"))
        else:
            return "Email ou mot de passe incorrect"

    return render_template("admin/login.html")

# ============================================================
# ADMINISTRATION - DASHBOARD ET LOGIN
# ============================================================
@app.route('/admin/dashboard', endpoint='admin_dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

#============================================================
# ADMINISTRATION - GESTION DES ACTUALITÉS (CRUD complet)
# ============================================================

@app.route("/admin/gerer_actualites")
def gerer_actualites():
    db = get_db()
    liste_actualites = db.execute("SELECT * FROM actualites ORDER BY date DESC").fetchall()
    return render_template("admin/gerer_actualites.html", actualites=liste_actualites)

# Ajouter une actualité
@app.route("/admin/ajouter_actualite", methods=["POST"])
def ajouter_actualite():

    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        INSERT INTO actualites
        (titre, date, description, photo)
        VALUES (?, ?, ?, ?)
        """,
        (titre, date, description, photo)
    )

    db.commit()

    return redirect(url_for("gerer_actualites"))


# Modifier une actualité
@app.route("/admin/modifier_actualite/<int:id>", methods=["POST"])
def modifier_actualite(id):

    titre = request.form["titre"]
    date = request.form["date"]
    description = request.form["description"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        UPDATE actualites
        SET titre=?, date=?, description=?, photo=?
        WHERE id=?
        """,
        (titre, date, description, photo, id)
    )

    db.commit()

    return redirect(url_for("gerer_actualites"))


# Supprimer une actualité
@app.route("/admin/supprimer_actualite/<int:id>", methods=["POST"])
def supprimer_actualite(id):

    db = get_db()

    db.execute(
        "DELETE FROM actualites WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("gerer_actualites"))

#============================================================
# ADMINISTRATION - GESTION DES ACTIVITES (CRUD complet)
# ============================================================

@app.route("/admin/gerer_activites")
def gerer_activites():
    db = get_db()
    liste_activites = db.execute("SELECT * FROM activites ORDER BY date DESC").fetchall()
    return render_template("admin/gerer_activites.html", activites=liste_activites)

# Ajouter une activite
@app.route("/admin/ajouter_activite", methods=["POST"])
def ajouter_activite():

    titre = request.form["titre"]
    date = request.form["date"]
    lieu = request.form["lieu"]
    organisateur = request.form["organisateur"]
    description = request.form["description"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        INSERT INTO activites
        (titre, date, lieu, organisateur, description, photo)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (titre, date, lieu, organisateur, description, photo,)
    )

    db.commit()

    return redirect(url_for("gerer_activites"))


# Modifier une activite
@app.route("/admin/modifier_activite/<int:id>", methods=["POST"])
def modifier_activite(id):

    titre = request.form["titre"]
    date = request.form["date"]
    lieu = request.form["lieu"]
    organisateur = request.form["organisateur"]
    description = request.form["description"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        UPDATE activites
        SET titre=?, date=?, lieu=?, organisateur=?, description=?, photo=?
        WHERE id=?
        """,
        (titre, date, lieu, organisateur, description, photo, id)
    )

    db.commit()

    return redirect(url_for("gerer_activites"))


# Supprimer une activite
@app.route("/admin/supprimer_activite/<int:id>", methods=["POST"])
def supprimer_activite(id):

    db = get_db()

    db.execute(
        "DELETE FROM activites WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("gerer_activites"))

#============================================================
#ADMINISTRATION - GESTION DES FORMATIONS (CRUD complet) 
# ============================================================

@app.route('/admin/gerer_formations')
def gerer_formations():
    db = get_db()
    liste_formations = db.execute("SELECT * FROM formations").fetchall()
    return render_template("admin/gerer_formations.html", formations=liste_formations)

# Ajouter une formation
@app.route("/admin/ajouter_formation", methods=["POST"])
def ajouter_formation():

    niveau = request.form["niveau"]
    nom = request.form["nom"]
    description = request.form["description"]

    db = get_db()

    db.execute(
        """
        INSERT INTO formations
        (niveau, nom, description)
        VALUES (?, ?, ?)
        """,
        (niveau, nom, description)
    )

    db.commit()

    return redirect(url_for("gerer_formations"))


# Modifier une formation
@app.route("/admin/modifier_formation/<int:id>", methods=["POST"])
def modifier_formation(id):

    niveau = request.form["niveau"]
    nom = request.form["nom"]
    description = request.form["description"]

    db = get_db()

    db.execute(
        """
        UPDATE formations
        SET niveau=?, nom=?, description=?
        WHERE id=?
        """,
        (niveau, nom, description, id)
    )

    db.commit()

    return redirect(url_for("gerer_formations"))


# Supprimer une formation
@app.route("/admin/supprimer_formation/<int:id>", methods=["POST"])
def supprimer_formation(id):

    db = get_db()

    db.execute(
        "DELETE FROM formations WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("gerer_formations"))

# ============================================================
# ADMINISTRATION - GESTION DES PHOTOS (CRUD)
# ============================================================

# Afficher les photos
@app.route("/admin/gerer_photos")
def gerer_photos():
    db = get_db()
    liste_photos = db.execute("SELECT * FROM galerie").fetchall()
    return render_template(
        "admin/gerer_photos.html",
        photos=liste_photos
    )


# Ajouter une photo
@app.route("/admin/ajouter_photo", methods=["POST"])
def ajouter_photo():

    titre = request.form["titre"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        INSERT INTO galerie
        (titre, photo)
        VALUES (?, ?)
        """,
        (titre, photo)
    )

    db.commit()

    return redirect(url_for("gerer_photos"))


# Modifier une photo
@app.route("/admin/modifier_photo/<int:id>", methods=["POST"])
def modifier_photo(id):

    titre = request.form["titre"]
    photo = request.form["photo"]

    db = get_db()

    db.execute(
        """
        UPDATE galerie
        SET titre=?, photo=?
        WHERE id=?
        """,
        (titre, photo, id)
    )

    db.commit()

    return redirect(url_for("gerer_photos"))


# Supprimer une photo
@app.route("/admin/supprimer_photo/<int:id>", methods=["POST"])
def supprimer_photo(id):

    db = get_db()

    db.execute(
        "DELETE FROM galerie WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("gerer_photos"))



for rule in app.url_map.iter_rules():
    print(rule.endpoint, "=>", rule)

if __name__ == "__main__":
    app.run(debug=True, port=5000)