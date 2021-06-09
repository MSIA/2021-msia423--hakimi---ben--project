import logging

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def createModel(features, target, rfRandState, splitRandState, n_est, mx_d, test_sz):
    """
    Build a random forest model and create test set

    Args:
        features: dataframe, required, dataframe of all input values for model
        target: dataframe, required, one column datafame of output (0, 1)
        rfRandState: (int), required, starting point to set seed for model
        splitRandState: (int), required, starting point to set seed for spliting data
        n_est: (int), required, number of estimators in random forest
        mx_d: (int), required, max depth of random forest
        test_sz: (double), between 0 and 1, required, proportion of data in test set

    Returns:
        random forset model, test set of predictors, test set of dependent variables
    """
    try:
        rf = RandomForestClassifier(n_estimators=n_est, max_depth=mx_d, random_state=rfRandState)
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
            features, target, test_size=test_sz, random_state=splitRandState)
        rf.fit(X_train, y_train)
        logger.info("Succesfully created model")
        return rf, X_test, y_test
    except:
        logger.error("Unable to create model")

def scoreModel(rf, X_test, y_test):
    """
    Provide model evaluation metrics for Random Forest model produced in createModel function

    Args:
        rf: (model), required, model produced from createModel function
        X_test: dataframe, required, test inputs for model
        y_test: dataframe, required, test outputs for model

    Returns:
        accuracy
    """
    try:
        ypred_bin_test = rf.predict(X_test)
        accuracy = accuracy_score(y_test, ypred_bin_test)
        logger.info("Succesfully scored model with accuracy = %s", str(accuracy))
        return accuracy
    except:
        logger.error("Unable to score model")
