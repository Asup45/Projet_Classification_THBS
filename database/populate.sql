-- Créer une table temporaire pour stocker les enregistrements sélectionnés aléatoirement
CREATE TEMPORARY TABLE temp_selected_records AS (
    SELECT * FROM transactions_fraude
    ORDER BY RAND()
    LIMIT 15
);

-- Mettre à jour la valeur dans chaque enregistrement sélectionné
UPDATE temp_selected_records
SET IsFraud = null;

-- Insérer les enregistrements modifiés dans la table de destination
INSERT INTO transactions_utilisateur
SELECT * FROM temp_selected_records;

-- Supprimer la table temporaire
DROP TEMPORARY TABLE IF EXISTS temp_selected_records;
