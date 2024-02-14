CREATE TABLE Typepaiment(
   typeID INT,
   Libelle VARCHAR(150),
   PRIMARY KEY(typeID)
);

CREATE TABLE Transactions(
   transactionID INT,
   step INT,
   amount INT,
   NameOrig VARCHAR(150),
   oldbalanceOrg DOUBLE,
   newbalanceOrig DOUBLE,
   nameDest VARCHAR(150),
   oldbalanceDest DOUBLE,
   newbalanceDest DOUBLE,
   IsFraud LOGICAL,
   typeID INT NOT NULL,
   PRIMARY KEY(transactionID),
   FOREIGN KEY(typeID) REFERENCES Typepaiment(typeID)
);
