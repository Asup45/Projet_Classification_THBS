import pandas as pd

from sklearn.model_selection import train_test_split

transactions = pd.read_csv('../database/transactions.csv', index_col='transactionId')

X = transactions.drop(columns=['isFraud', 'nameOrig', 'nameDest'])
y = transactions['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)