from datainit import *

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


def calc_metrics(name, model):
    y_pred = model.predict(X_test)

    return [
        name,
        model.score(X_test, y_test),
        recall_score(y_test, y_pred),
        precision_score(y_test, y_pred),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    ]