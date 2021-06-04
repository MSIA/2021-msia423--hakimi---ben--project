import logging

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score

def createModel(features, target):
    rf = RandomForestClassifier(n_estimators=20, max_depth=5, random_state=9876)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        features, target, test_size=0.25, random_state=1234)
    rf.fit(X_train, y_train)
    return rf, X_test, y_test

def scoreModel(rf, X_test, y_test):
    # ypred_proba_test = rf.predict_proba(X_test)[:,1]
    ypred_bin_test = rf.predict(X_test)
    # auc = roc_auc_score(y_test, ypred_proba_test)
    #confusion = confusion_matrix(y_test, ypred_bin_test)
    accuracy = accuracy_score(y_test, ypred_bin_test)
    return accuracy
