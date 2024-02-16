import pandas as pd

def norm2float(df:pd.DataFrame, cols:list):
    for col in cols:
        df[col] = df[col].str.replace(',', '.').astype(float)
        
    return df

transactions = pd.read_csv('../res/credit_card_fraud.csv', sep=';', index_col='transactionId')
transactions[['type']] = transactions[['type']].replace(['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'], range(0, 5))
transactions = norm2float(transactions, ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'])
transactions.to_csv('../database/transactions.csv', index='transactionId', sep=',')