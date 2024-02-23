import flask
import pickle
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for,flash
from flask import session #pour recuperer donnée de session comme le nom utilisateur
import mysql.connector as msql
from mysql.connector import Error
import subprocess

app = Flask(__name__)
app.secret_key = 'azerty'

# Charger votre modèle pré-entrainé
with open(r'C:\Users\Utilisateur2\Documents\FORM-DEVIA\3-CLASSIFICATION\7Projet\github\Projet_Classification_THBS\database\modele\XGBmodel.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Configuration de la connexion à MySQL
config_bdd = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'projet_fraudedb'
}

# pour client et opérateur:Fonction pour valider les identifiants de l'utilisateur dans bdd
def valider_utilisateur(nom_utilisateur, mot_de_passe):
    try:
        conn = msql.connect(**config_bdd)
        curseur = conn.cursor()
        requete = "SELECT email, pass, role FROM utilisateur WHERE email = %s AND pass = %s"
        curseur.execute(requete, (nom_utilisateur, mot_de_passe))
        utilisateur = curseur.fetchone()
        curseur.close()
        conn.close()
        return utilisateur
    except Error as err:
        print(f"Erreur : {err}")
        return None

    
# seulement pour client:Fonction pour creer (ou maj password) les identifiants de l'utilisateur dans bdd
def creer_utilisateur(nom_utilisateur, mot_de_passe,role):
    try:
        conn = msql.connect(**config_bdd)
        cursor = conn.cursor()

        # Vérifier si l'utilisateur existe
        requete_utilisateur = "SELECT email, pass, role FROM utilisateur WHERE email = %s"
        cursor.execute(requete_utilisateur, (nom_utilisateur,))
        existe_utilisateur = cursor.fetchone()

        if existe_utilisateur:
            # L'utilisateur existe mettre à jour le mot de passe
            maj_requete = "UPDATE utilisateur SET pass= %s WHERE email = %s"
            cursor.execute(maj_requete, (mot_de_passe, nom_utilisateur))
        else:
            # L'utilisateur n'existe pas: le créer
            insertion_requete = "INSERT INTO utilisateur (email, pass,role) VALUES (%s, %s,%s)"
            cursor.execute(insertion_requete, (nom_utilisateur, mot_de_passe,role))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Erreur : {err}")
        return False
    
def load_data_from_database():
    # Se connecter à votre base de données MySQL
    conn = msql.connect(**config_bdd)
    
    # Créer un curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()
    
    # Exécuter la requête SQL pour récupérer les données
    query = "SELECT * FROM transactions_utilisateur WHERE IsFraud IS NULL;"
    cursor.execute(query)
    
    # Récupérer les résultats de la requête et les stocker dans un DataFrame pandas
    data = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    # Récupérer les valeurs distinctes de nameOrig
    nameOrig_options = data['nameOrig'].unique().tolist()
    # Fermer le curseur et la connexion à la base de données
    cursor.close()
    conn.close()
    
    return data, nameOrig_options

def mettre_a_jour_isfraud_en_bloc(data):
    try:
        conn = msql.connect(**config_bdd)
        cursor = conn.cursor()

        # Création d'une liste de tuples (nouvelle_valeur_isfraud, transaction_id)
        valeurs_a_mettre_a_jour = [(row['IsFraud'], row['transactionId']) for index, row in data.iterrows()]

        # Création de la requête SQL pour la mise à jour en bloc
        mise_a_jour_requete = """
            UPDATE transactions_utilisateur 
            SET IsFraud = CASE 
                %s 
                ELSE IsFraud 
            END
            WHERE transactionId IN (%s)
        """
        
        # Construction des parties de la requête pour les valeurs et les identifiants
        valeurs_sql = " ".join(["WHEN %s THEN %s" % (item[1], item[0]) for item in valeurs_a_mettre_a_jour])
        identifiants_sql = ", ".join(["%s" for item in valeurs_a_mettre_a_jour])

        # Exécution de la requête
        cursor.execute(mise_a_jour_requete % (valeurs_sql, identifiants_sql), [item[1] for item in valeurs_a_mettre_a_jour])

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"Erreur : {err}")
        return False




# Insérer la ligne admin@moneyshied.fr, admin, operateur s'il n'existe pas
if not valider_utilisateur('admin@moneyshield.fr', 'admin'):
    creer_utilisateur('admin@moneyshield.fr', 'admin', 'operateur')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
# formulaire operateur(connexion)/client(connexion-inscription) 
def connexion():
    print("form :",request.form['email'])
    print("form :",request.form['password'])
    print("form :",request.form['validation'])
    nom_utilisateur = request.form['email']
    mot_de_passe = request.form['password']
    validation_type = request.form['validation']
    if validation_type == 'connexion':
    #if request.form['validation']=='connexion': # client/operateur en mode connexion 
        utilisateur = valider_utilisateur(nom_utilisateur, mot_de_passe)

        if utilisateur:
            session['utilisateur'] = nom_utilisateur  # Ajout du nom d'utilisateur à la session pour recuperer dans template
            # Identifiants valides, rediriger en fonction du rôle
            if utilisateur[2] == 'operateur': #test du role operateur pour identification pour renvoyer sur  prediction
                
                return redirect(url_for('prediction')) 
            else:                             #test du role client pour identification pour renvoyer sur  transaction
                #return render_template('transaction.html')
                return redirect(url_for('transaction')) 

        else:
            # Identifiants invalides=> index avec message erreur
            flash("Identifiants invalides. Veuillez réessayer.")
            return render_template('index.html')
        
    else:  # si ce n'est pas une connexion alors client en mode creation
        nom_utilisateur = request.form['email']
        mot_de_passe = request.form['password']

        utilisateur = creer_utilisateur(nom_utilisateur, mot_de_passe,'client')

        if utilisateur:
            session['utilisateur'] = nom_utilisateur  # Ajout du nom d'utilisateur à la session pour recuperer dans template
            # creation client et Identifiant valide 
            return redirect(url_for('transaction')) 
        else:
            # creation invalide=> index avec message erreur
            flash("Problème création client. Veuillez réessayer")
            return render_template('index.html') 
               
#@app.route('/prediction', methods=['GET'])
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    data, nameOrig_options = load_data_from_database() #data et filtre
    #print("data:", data)
    #print("data before filtering:", data)#verifie avant filtre

    # Supprimer la colonne "IsFraud" si elle existe
    if 'IsFraud' in data.columns:
        data.drop(columns=['IsFraud'], inplace=True)
        # Copier la colonne transactionId avant de la supprimer
        transactionId_backup = data['transactionId'].copy()
        data.drop(columns=['transactionId'],inplace=True)
    
    # Faire des prédictions
    predictions = model.predict(data)
    
    # Ajouter les prédictions à vos données
    data['IsFraud'] = predictions.tolist()

    #print("data:", data)
    #print("Unique values in nameOrig:", data['nameOrig'].unique().tolist()) #verifie la source de la liste

    
    if request.method == 'POST':
        selected_filter = request.form.get('filter', '')
        print("selected_filter:", selected_filter)#pour verif filtre selectionné
        # Filtrer les données en fonction du filtre
        if selected_filter:
            #filtered_data = data[data['nameOrig'] == selected_filter]
            filtered_data = data[data['nameOrig'].astype(float) == float(selected_filter)]
        else:
            filtered_data = data
    else:
        selected_filter = ''
        filtered_data = data

    #print("filtered_data:", filtered_data)#pour verif data filtré
    data = pd.concat([data, transactionId_backup], axis=1)
    data.rename(columns={'transactionId_backup': 'transactionId'}, inplace=True)
    #print("Data:", data)

    # Boucle pour mettre à jour la base de données avec les nouvelles valeurs de IsFraud
    mettre_a_jour_isfraud_en_bloc(data)

    #return render_template('prediction.html', data=data, nameOrig_options=nameOrig_options)
    # Renvoyer les données filtrées et les options de filtre au template
    # Ajouter la colonne sauvegardée à la fin du DataFrame
    
    return render_template('prediction.html', data=filtered_data, nameOrig_options=nameOrig_options, selected_filter=selected_filter)

#integrer dans le template {% with messages = get_flashed_messages() %} et {% for message in messages %} pour visualiser les messages

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        flash("Transaction effectuée")
        return render_template('transaction.html')
    else:
        # Traitement spécifique pour la méthode GET
        # Peut-être rediriger vers une autre page ou effectuer d'autres actions
        return render_template('transaction.html')  # Ou rediriger vers une autre page



@app.route('/run_populate_script', methods=['POST'])
def run_populate_script():
    script_name = request.form.get('scriptName', 'populate.py')

    try:
        # Utilisez subprocess pour exécuter le script Python
        subprocess.run(['python', script_name])

        # Rediriger vers la page prediction.html
        return redirect(url_for('prediction'))
    except Exception as e:
        # En cas d'erreur, vous pouvez également rediriger vers prediction.html ou afficher un message d'erreur
        return redirect(url_for('prediction'))

if __name__ == '__main__':
    app.run(debug=True)
