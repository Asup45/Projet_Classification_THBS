import pandas as pd
from helpers import *

transactions = pd.read_csv('../res/credit_card_fraud.csv', sep=';', index_col='transactionId')

transactions[['type']] = transactions[['type']].replace(['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'], range(0, 5))
transactions['nameOrig'] = transactions['nameOrig'].apply(replace_first_letter)
transactions['nameDest'] = transactions['nameDest'].apply(replace_first_letter)
transactions = norm2float(transactions, ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'nameOrig', 'nameDest'])

transactions.to_csv('../database/transactions.csv', index='transactionId', sep=',')