CREATE TABLE transactions_utilisateur (
    transactionId INT NOT NULL PRIMARY KEY,
    step INT,
    type INT NOT NULL,
    amount FLOAT,
    nameOrig FLOAT,
    oldbalanceOrg FLOAT,
    newbalanceOrig FLOAT,
    nameDest FLOAT,
    oldbalanceDest FLOAT,
    newbalanceDest FLOAT,
    IsFraud INT
);
