#pip install mysql-connector-python
#pip install pandas
#script permettant la creation et alimentation des données à partir du MCD et du fichier brut credit_card_fraud_corr.csv (fichier origine card_credit_fraud_Classification project Final.csv formaté avec ;)

#DEBUT import des bibliotheques nécessaires
import mysql.connector as msql
import pandas as pd
from mysql.connector import Error
#FIN import des bibliotheques nécessaires

# Codes ANSI pour les couleurs du texte
RESET = "\033[0m"
YELLOW = "\033[93m"

# Demander la valeur de xroot à l'utilisateur pour la connexion à la bd
xroot = input("Entrez le user pour la connexion BD : ")
# Demander la valeur de xpass à l'utilisateur
xpass = input("Entrez le mot de pass : ")
msg="Problème de connexion MySQL"

#DEBUT Creation bdd Projet_Fraude selon schema MCD
try:
    conn = msql.connect(host='localhost', user=xroot, password=xpass)
    if conn.is_connected():
        cursor = conn.cursor()
        print("Vous êtes  sur MYSQL")
        cursor.execute('DROP DATABASE IF EXISTS projet_fraudedb;')
        cursor.execute("CREATE DATABASE projet_fraudedb")
        print("la base projet_Fraude est créee")
        cursor.execute("USE projet_fraudedb")
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Vous êtes connecté à la base: ", record)
 
except Error as e:
    print(msg, e)
#FIN Creation bdd Projet_Fraude

#DEBUT Creation structure des tables  Typepaiment et Transaction_Fraud
try:    
    cursor.execute('DROP TABLE IF EXISTS credit_card_fraud_corr;')
    cursor.execute('DROP TABLE IF EXISTS transaction_fraude;') #suppression dans cette ordre car clef etrangere
    cursor.execute('DROP TABLE IF EXISTS typepaiment;')
    cursor.execute('DROP TABLE IF EXISTS utilisateur;')
    cursor.execute('DROP TABLE IF EXISTS transactions_utilisateur;')

    print(f"{YELLOW}")
    print('Création de la table credit_card_fraud_corr en cours....')
    cursor.execute("CREATE TABLE credit_card_fraud_corr (transactionID INT, step INT, type VARCHAR(50),amount FLOAT,NameOrig VARCHAR(150),oldbalanceOrg FLOAT,newbalanceOrig FLOAT,nameDest VARCHAR(150),oldbalanceDest FLOAT,newbalanceDest FLOAT,IsFraud INT)")
    print('La table credit_card_fraud_corr est crée....')

    print('Création de la table typepaiment en cours....') #creer la table typepaiment en premier car clef etrangere référencé dans transaction_fraude
    cursor.execute("CREATE TABLE typepaiment(typeID INT, Libelle VARCHAR(150), PRIMARY KEY(typeID))")
    print("La table typepaiment est crée....")

    print('Création de la table transaction_fraude en cours....')
    cursor.execute("CREATE TABLE transaction_fraude (transactionID INT,step INT,amount FLOAT,NameOrig VARCHAR(150),oldbalanceOrg FLOAT,newbalanceOrig FLOAT,nameDest VARCHAR(150),oldbalanceDest FLOAT,newbalanceDest FLOAT,IsFraud INT,typeID INT NOT NULL,PRIMARY KEY(transactionID),FOREIGN KEY(typeID) REFERENCES typepaiment(typeID))")
    print("La table transaction_fraude est crée....")

    print('Création de la table transactions_utilisateur en cours....')
    cursor.execute("CREATE TABLE transactions_utilisateur (transactionID INT,step INT,amount FLOAT,NameOrig VARCHAR(150),oldbalanceOrg FLOAT,newbalanceOrig FLOAT,nameDest VARCHAR(150),oldbalanceDest FLOAT,newbalanceDest FLOAT,IsFraud INT,typeID INT NOT NULL,PRIMARY KEY(transactionID))")
    print("La table transactions_utilisateur est crée....")

    print('Création de la table utilisateur en cours....') #creer la table utilisateur
    cursor.execute("CREATE TABLE utilisateur(email VARCHAR(50), pass VARCHAR(150), role VARCHAR(150), PRIMARY KEY(email))")
    print("La table utilisateur est crée....")
    print(f"{RESET}")
except Error as e:
    print(msg, e)
#FIN Creation structure des tables Typepaiment et Transaction_Fraud

#DEBUT chargement de credit_card_fraud_corr.csv dans la table credit_card_fraud_corr

# Importe en fonction du nombre de ligne à traiter xlignecsv (exemple saisir la valeur pour les 10 premieres lignes du csv ou  ssaisir 0 pour tous le fichier) et parametre nrows 
# l'utilité de saisir le nombre de ligne permet de tester la creation de la bdd sur un nombrre restreint en cas de prb 
xlignecsv = int(input("Combien de lignes à traiter à partir du fichier csv ? (saisir 0 pour tout le fichier csv):"))
if xlignecsv==0:
    print("Vous allez traiter tout le fichier")
    transactionData = pd.read_csv('credit_card_fraud_corr.csv', index_col=False, delimiter=';')
else:
    print("Vous allez traiter ",xlignecsv," lignes")
    transactionData = pd.read_csv('credit_card_fraud_corr.csv', index_col=False, delimiter=';', nrows=int(xlignecsv))
    
#pretraitement
#remplace , par . pour les nombres
transactionData['amount'] = transactionData['amount'].replace(',', '.', regex=True).astype(float)
transactionData['oldbalanceOrg'] = transactionData['oldbalanceOrg'].replace(',', '.', regex=True).astype(float)
transactionData['newbalanceOrig'] = transactionData['newbalanceOrig'].replace(',', '.', regex=True).astype(float)
transactionData['oldbalanceDest'] = transactionData['oldbalanceDest'].replace(',', '.', regex=True).astype(float)
transactionData['newbalanceDest'] = transactionData['newbalanceDest'].replace(',', '.', regex=True).astype(float)

# Remplacer les lettres 'c' dans la colonne 'nameOrig' par '1'
transactionData['nameOrig'] = transactionData['nameOrig'].str.replace('C', '1')

# Remplacer les lettres 'c' dans la colonne 'nameDest' par '1'
transactionData['nameDest'] = transactionData['nameDest'].str.replace('C', '1')

# Remplacer les lettres 'm' dans la colonne 'nameDest' par '2'
transactionData['nameDest'] = transactionData['nameDest'].str.replace('M', '2')

# Afficher les premières lignes du DataFrame pour vérifier les modifications
transactionData.head(10)

try:
    #alimente la table credit_card_fraud_corr  à partir du dataframe
    for i,row in transactionData.iterrows():                     
        sql = "INSERT INTO projet_fraudedb.credit_card_fraud_corr VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
    conn.commit() #il vaut faire le commit à la fin de tous les insertion, on gagne bcp en performance
    print(f"{YELLOW}")
    print("les lignes de la dataframe (credit_card_fraud_corr.csv) ont été insérées dans la table credit_card_fraud_corr")

    #affiche les 5 premieres ligne de la table credit_card_fraud_corr 
    cursor.execute("select * from projet_fraudedb.credit_card_fraud_corr limit 5")
    result=cursor.fetchall()
    print("Affichage des 5 premières lignes de la table credit_card_fraud_corr: ")
    for i in result:
        print(result)
    print(f"{RESET}")
except Error as e:
    print(msg, e)
#FIN chargement de credit_card_fraud_corr.csv dans la table credit_card_fraud_corr
    
# DEBUT insertion des types de paiement dans la table typepaiment
try:
    cursor.execute("delete from typepaiment")
    cursor.execute("INSERT INTO typepaiment (typeID, Libelle) VALUES (1 , 'PAYMENT')")
    cursor.execute("INSERT INTO typepaiment (typeID, Libelle) VALUES (2 , 'TRANSFER')")
    cursor.execute("INSERT INTO typepaiment (typeID, Libelle) VALUES (3 , 'CASH_OUT')")
    cursor.execute("INSERT INTO typepaiment (typeID, Libelle) VALUES (4 , 'CASH_IN')")
    cursor.execute("INSERT INTO typepaiment (typeID, Libelle) VALUES (5 , 'DEBIT')")
    conn.commit()
    print("Les différents types de paiement ont été integrés dans la table typepaiment")

except Error as e:
    print(msg, e)
#FIN insertion des types de paiement dans la table typepaiment
    
#DEBUT alimentation de la transaction_fraude à partir de credit_card_fraud_corr et typepaiment 
try:        
    # Récupération des données de la table credit_card_fraud_corr
    cursor.execute("SELECT * FROM credit_card_fraud_corr")
    transactions = cursor.fetchall()

    # Récupération des données de la table typepaiment
    cursor.execute("SELECT * FROM typepaiment")
    types_paiement = cursor.fetchall()

    # Parcours des transactions et insertion dans la table transaction_fraude
    for transaction in transactions:
        for type_paiement in types_paiement:
            if transaction[2] == type_paiement[1]:  # Vérification du type de paiement
                # Insertion de la transaction avec le type de paiement correspondant
                cursor.execute("INSERT INTO transaction_fraude (transactionID, step, amount, NameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, IsFraud, typeID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (transaction[0], transaction[1], transaction[3], transaction[4], transaction[5], transaction[6], transaction[7], transaction[8], transaction[9], transaction[10], type_paiement[0]))
                
                break  # Sortir de la boucle une fois que le type de paiement correspondant est trouvé
    conn.commit()
    print(f"{YELLOW}")
    print("Les données ont été insérées dans la table transaction_fraude.")
    
except Error as e:
    print(msg, e)

finally:
    # Fermeture de la connexion
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connexion à la base de données fermée.")
        print(f"{RESET}")

