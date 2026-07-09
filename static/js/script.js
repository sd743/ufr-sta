// Sélection des boutons
const boutons = document.querySelectorAll(".categories button");

// Sélection des cartes
const cartes = document.querySelectorAll(".card");

// Parcours des boutons
boutons.forEach(bouton => {

    bouton.addEventListener("click", () => {

        // Supprimer la classe active
        boutons.forEach(btn => btn.classList.remove("active"));

        // Ajouter la classe active
        bouton.classList.add("active");

        // Catégorie choisie
        const filtre = bouton.dataset.filter;

        cartes.forEach(carte => {

            if (filtre === "all") {

                carte.style.display = "block";

            }

            else if (carte.dataset.category === filtre) {

                carte.style.display = "block";

            }

            else {

                carte.style.display = "none";

            }

        });

    });

});