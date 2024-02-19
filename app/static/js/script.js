// Sélectionner les boutons radio
const clientRadio = document.getElementById('client');
const operateurRadio = document.getElementById('operateur');

// Sélectionner les éléments nécessaires pour afficher les formulaires
const choixclientDiv = document.getElementById('choixclient');
const formulaireInscription = document.getElementById('formulaireInscription');
const formulaireConnexion = document.getElementById('formulaireConnexion');

// Ajouter un écouteur d'événement pour détecter les changements de sélection
clientRadio.addEventListener('change', function() {
    // Action à effectuer lorsque l'utilisateur choisit "Utilisateur"
    console.log('client sélectionné');
    if (clientRadio.checked) {
        choixclientDiv.style.display = 'block';
        formulaireInscription.style.display = 'none';
        formulaireConnexion.style.display = 'none';
    }
});

operateurRadio.addEventListener('change', function() {
    // Action à effectuer lorsque l'utilisateur choisit "Opérateur"
    console.log('Opérateur sélectionné');
    if (operateurRadio.checked) {
        choixclientDiv.style.display = 'none';
        formulaireConnexion.style.display = 'block';
    }
});

// Ajouter des écouteurs d'événement pour les choix de l'utilisateur
document.getElementById('inscription').addEventListener('click', function() {
    formulaireInscription.style.display = 'block';
    formulaireConnexion.style.display = 'none';
});

document.getElementById('connexion').addEventListener('click', function() {
    formulaireInscription.style.display = 'none';
    formulaireConnexion.style.display = 'block';
});
