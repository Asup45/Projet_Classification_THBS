import mysql.connector

# Configuration de la connexion à MySQL
config_bdd = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'projet_fraudedb'
}

# Script SQL à exécuter
script_sql = """
USE projet_fraudedb;
DROP TEMPORARY TABLE IF EXISTS projet_fraudedb.temp_selected_records;
CREATE TEMPORARY TABLE temp_selected_records AS (
    SELECT * FROM projet_fraudedb.transaction_fraude
    ORDER BY rand()
    LIMIT 100
);
UPDATE projet_fraudedb.temp_selected_records
SET IsFraud = null  WHERE IsFraud=1;
UPDATE projet_fraudedb.temp_selected_records
SET IsFraud = null  WHERE IsFraud=0;
INSERT INTO projet_fraudedb.transactions_utilisateur
SELECT * FROM projet_fraudedb.temp_selected_records;
DROP TEMPORARY TABLE IF EXISTS projet_fraudedb.temp_selected_records;
"""

# Fonction pour exécuter le script SQL
def executer_script_sql(conn, script):
    cursor = conn.cursor()
    try:
        # Diviser le script en commandes individuelles
        commands = [command.strip() for command in script.split(';') if command.strip()]
        
        # Exécuter chaque commande séparément
        for command in commands:
            cursor.execute(command)
        
        conn.commit()
        print("Script SQL exécuté avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur d'exécution du script SQL : {err}")
    finally:
        cursor.close()

# Connexion à la base de données
try:
    connexion_bdd = mysql.connector.connect(**config_bdd)
    executer_script_sql(connexion_bdd, script_sql)
finally:
    if connexion_bdd.is_connected():
        connexion_bdd.close()
