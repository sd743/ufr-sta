// Exemple : menu déroulant
document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");

    if (toggle && menu) {
        toggle.addEventListener("click", () => {
            menu.classList.toggle("active");
        });
    }
});

// Exemple : validation du formulaire contact
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".contact-form form");
    if (form) {
        form.addEventListener("submit", function(event) {
            const email = document.getElementById("email").value;
            if (!email.includes("@")) {
                alert("Veuillez entrer un email valide !");
                event.preventDefault();
            }
        });
    }
});
function toggleSidebar() {
    document.querySelector(".admin-sidebar").classList.toggle("active");
}



