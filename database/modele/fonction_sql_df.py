def sql_df(xroot,xpass,host,bdd,table,index_col): #fonction retournant le dataframe correspondant à la requete
    import pandas as pd 
    from sqlalchemy import create_engine

    # Créer une URI de base de données pour SQLAlchemy
    uri = f"mysql+pymysql://{xroot}:{xpass}@{host}/{bdd}"

    # Créer un moteur de base de données SQLAlchemy
    engine = create_engine(uri)

    # Votre requête SQL
    requete_sql = f"SELECT * FROM {table};"

    # Utilisation de pandas pour exécuter la requête SQL et remplir un DataFrame
    data = pd.read_sql_query(requete_sql, engine, index_col="transactionID")

    # Fermer la connexion au moteur de base de données SQLAlchemy
    engine.dispose()
    return data