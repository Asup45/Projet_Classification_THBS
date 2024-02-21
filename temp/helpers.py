import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


transactions = pd.read_csv('../database/transactions.csv', index_col='transactionId')

X = transactions.drop(columns=['isFraud'])
y = transactions['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def calc_metrics(name, model):
    y_pred = model.predict(X_test)

    return [
        name,
        model.score(X_test, y_test),
        recall_score(y_test, y_pred),
        precision_score(y_test, y_pred, zero_division=1),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    ]

def replace_first_letter(value):
    if value.startswith('C'):
        return '1' + value[1:]
    elif value.startswith('M'):
        return '2' + value[1:]
    else:
        return value
    
def norm2float(df:pd.DataFrame, cols:list):
    for col in cols:
        df[col] = df[col].str.replace(',', '.').astype(float)
        
    return df

def norm2int(df:pd.DataFrame, cols:list):
    for col in cols:
        df[col] = df[col].str.replace(',', '.').astype(int)
        
    return df