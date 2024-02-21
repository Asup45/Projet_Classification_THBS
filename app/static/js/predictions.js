// Récupérer les données depuis le modèle Python rendu dans la page HTML
const predictedData = {{ data | safe }};

// Récupérer les données prédites depuis le sessionStorage
const sessionData = JSON.parse(sessionStorage.getItem('data'));

// Sélectionner le corps de la table
const tableBody = document.getElementById('table-body');

// Nettoyer le contenu de la table
tableBody.innerHTML = '';

// Parcourir les données prédites et les ajouter à la table
predictedData.forEach(item => {
    const row = document.createElement('tr');
    
    // Créer une cellule pour chaque valeur prédite
    Object.values(item).forEach(value => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.appendChild(cell);
    });

    // Vérifier si la valeur de IsFraud est égale à 1
    if (item.IsFraud === 1) {
        row.classList.add('isfraud'); // Ajouter la classe isfraud à la ligne
    }
    
    // Ajouter la ligne à la table
    tableBody.appendChild(row);
});

// Récupérer l'élément du menu déroulant
const nameSelector = document.getElementById('verif');

// Parcourir les données et ajouter chaque nom comme une option dans le menu déroulant
sessionData.forEach(item => {
    // Créer une nouvelle option
    const option = document.createElement('option');
    // Définir la valeur et le texte de l'option avec le nom de l'item
    option.value = item.nameOrig; // Assurez-vous d'ajuster ceci en fonction de la structure de vos données
    option.textContent = item.nameOrig; // Assurez-vous d'ajuster ceci en fonction de la structure de vos données
    // Ajouter l'option au menu déroulant
    nameSelector.appendChild(option);
});

// Fonction de filtrage des données
function filterData() {
    const selectedValue = nameSelector.value;
    const filteredData = predictedData.filter(item => item.nameOrig === selectedValue);
    
    // Afficher les données filtrées dans votre interface utilisateur
    displayFilteredData(filteredData);
}

// Afficher les données filtrées dans votre interface utilisateur
function displayFilteredData(filteredData) {
    tableBody.innerHTML = ''; // Nettoyer le contenu de la table
    
    // Parcourir les données filtrées et les ajouter à la table
    filteredData.forEach(item => {
        const row = document.createElement('tr');
        
        // Créer et ajouter les cellules avec les données correspondantes
        Object.values(item).forEach(value => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });
        
        // Vérifier si la valeur de IsFraud est égale à 1
        if (item.IsFraud === 1) {
            row.classList.add('isfraud'); // Ajouter la classe isfraud à la ligne
        }
        
        // Ajouter la ligne à la table
        tableBody.appendChild(row);
    });
}

// Appeler la fonction de filtrage lorsque la valeur du select change
nameSelector.addEventListener('change', filterData);
