import sqlite3
# Connexion à la base de données
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
# ==========================
# TABLE ADMINISTRATEURS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS administrateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL
)
""")
# ==========================
# TABLE ACTUALITES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS actualites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    photo TEXT
)
""")
# ==========================
# TABLE ACTIVITES
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS activites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    date TEXT NOT NULL,
    lieu TEXT NOT NULL,
    organisateur TEXT NOT NULL,
    description TEXT NOT NULL,
    photo TEXT
)
""")
# ==========================
# TABLE GALERIE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS galerie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    photo TEXT NOT NULL
)
""")
# ==========================
# TABLE FORMATIONS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS formations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    niveau TEXT NOT NULL,
    description TEXT NOT NULL
)
""")
# ==========================
# TABLE ENSEIGNANTS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS enseignants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    grade TEXT NOT NULL,
    departement TEXT NOT NULL,
    email TEXT NOT NULL,
    domaine TEXT NOT NULL,
    photo TEXT
)
""")
# ==========================
# ADMIN PAR DÉFAUT
# ==========================
cursor.execute("""
INSERT OR IGNORE INTO administrateurs(email, mot_de_passe)
VALUES('admin@ufrsta.com','admin123')
""")
conn.commit()
conn.close()
print("Base de données créée avec succès.")


