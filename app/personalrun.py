import flask
import pickle
import pandas as pd
from flask import Flask, render_template, request
import mysql.connector
import json

app = Flask(__name__)

# Charger votre modèle pré-entrainé
with open('XGBmodel.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Charger vos données depuis votre base de données
def load_data_from_database():
    # Se connecter à votre base de données MySQL
    conn = mysql.connector.connect(
        host="votre_host",
        user="votre_utilisateur",
        password="votre_mot_de_passe",
        database="votre_base_de_donnees"
    )
    
    # Créer un curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()
    
    # Exécuter la requête SQL pour récupérer les données
    query = "SELECT * FROM transactions_utilisateur WHERE IsFraud IS NULL;"
    cursor.execute(query)
    
    # Récupérer les résultats de la requête et les stocker dans un DataFrame pandas
    data = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    
    # Fermer le curseur et la connexion à la base de données
    cursor.close()
    conn.close()
    
    return data

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/predict', methods=['GET'])
def predictBase():
    data = load_data_from_database()
    # Supprimer la colonne "IsFraud" si elle existe
    if 'IsFraud' in data.columns:
        data.drop(columns=['IsFraud'], inplace=True)
    
    # Faire des prédictions
    predictions = model.predict(data)
    
    # Ajouter les prédictions à vos données
    data['IsFraud'] = predictions.tolist()
    
    # Renommer la colonne des prédictions
    return render_template('predict.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
