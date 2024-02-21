import flask
import pickle
import pandas as pd
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Charger votre modèle pré-entrainé
with open('XGBmodel.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Charger vos données depuis votre base de données
def load_data_from_database():
    # Logique pour se connecter à votre base de données et charger les données
    # Exemple :
    # data = pd.read_sql_query("SELECT * FROM ma_table;", my_database_connection)
    # return data
    # Pour cet exemple, nous utiliserons simplement un DataFrame fictif
    data = pd.DataFrame({'feature1': [value1, value2, ...], 'feature2': [value1, value2, ...], ...})
    return data

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Charger les données à partir de la base de données
        data = load_data_from_database()
        
        # Appliquer votre logique de prétraitement des données si nécessaire
        # data_processed = preprocess_data(data)
        
        # Faire des prédictions
        predictions = model.predict(data)
        
        # Ajouter les prédictions à votre DataFrame
        data['predictions'] = predictions
        
        # Retourner le résultat à la page de prédiction
        return render_template('predict.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
