USE   projet_fraudedb;
DROP TEMPORARY TABLE IF EXISTS projet_fraudedb.temp_selected_records;
CREATE TEMPORARY TABLE temp_selected_records AS (
    SELECT * FROM projet_fraudedb.transaction_fraude
    ORDER BY rand()
    LIMIT 15
);
UPDATE projet_fraudedb.temp_selected_records
SET IsFraud = null  WHERE IsFraud=1;
UPDATE projet_fraudedb.temp_selected_records
SET IsFraud = null  WHERE IsFraud=0;
INSERT INTO projet_fraudedb.transactions_utilisateur
SELECT * FROM projet_fraudedb.temp_selected_records;
DROP TEMPORARY TABLE IF EXISTS projet_fraudedb.temp_selected_records;
