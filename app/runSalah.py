import flask
from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector as msql
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'azerty'

# Configuration de la connexion à MySQL
config_bdd = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aqzsedrf21!87',
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
            # Identifiants valides, rediriger en fonction du rôle
            if utilisateur[2] == 'operateur': #test du role operateur pour identification pour renvoyer sur  prediction
                return render_template('prediction.html')
            else:                             #test du role client pour identification pour renvoyer sur  transaction
                return render_template('transaction.html')
        else:
            # Identifiants invalides=> index avec message erreur
            flash("Identifiants invalides. Veuillez réessayer.")
            return render_template('index.html')
        
    else:  # si ce n'est pas une connexion alors client en mode creation
        nom_utilisateur = request.form['email']
        mot_de_passe = request.form['password']

        utilisateur = creer_utilisateur(nom_utilisateur, mot_de_passe,'client')

        if utilisateur:
            # creation client et Identifiant valide 
            return render_template('transaction.html')
        else:
            # creation invalide=> index avec message erreur
            flash("Problème création client. Veuillez réessayer")
            return render_template('index.html')        

#integrer dans le template {% with messages = get_flashed_messages() %} et {% for message in messages %} pour visualiser les messages
        



if __name__ == '__main__':
    app.run(debug=True)
