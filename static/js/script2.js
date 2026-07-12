document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".contact-form form");

    if (form) {
        form.addEventListener("submit", function(event) {
            // Récupération des champs
            const nom = document.getElementById("nom").value.trim();
            const email = document.getElementById("email").value.trim();
            const sujet = document.getElementById("sujet").value.trim();
            const message = document.getElementById("message").value.trim();

            let erreurs = [];

            // Vérifications
            if (nom === "") {
                erreurs.push("Le nom complet est obligatoire.");
            }
            if (email === "" || !email.includes("@")) {
                erreurs.push("Veuillez entrer un email valide.");
            }
            if (sujet === "") {
                erreurs.push("Le sujet est obligatoire.");
            }
            if (message === "") {
                erreurs.push("Le message est obligatoire.");
            }

            // Gestion des erreurs
            if (erreurs.length > 0) {
                alert("⚠️ Erreurs détectées :\n\n" + erreurs.join("\n"));
                event.preventDefault(); // Empêche l’envoi
            } else {
                alert("✅ Votre message a été envoyé avec succès !");
            }
        });
    }
});
