from typing import Callable
import logging

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

__all__ = ['adaboost_m1',]

def adaboost_m1(X, y, clf = None, M = 500) ->  Callable:
    """
    AdaBoost.M1 algorithm.
    """

    if clf is None:
        clf = DecisionTreeClassifier(max_depth=1)

    #------ Cleaning ---------#
    y = y.reshape(-1)          

    #------ Setup ---------#             
    n = X.shape[0]
    w = np.ones(n)/n

    models = []
    for m in range(M):
        clf.fit(X, y, sample_weight=w)      # require sample_weight for fit
        y_pred = clf.predict(X)
        
        err = np.sum(w * (y != y_pred)) / np.sum(w)
        alpha = np.log((1 - err)/err)
        w = w * np.exp(alpha * (y != y_pred))
        # w = w * np.exp(alpha * ((y != y_pred) * 2 - 1))
        models.append((clf, alpha))

    def predict(X_new):
        y_pred = np.zeros(X_new.shape[0])
        for clf, alpha in models:
            y_pred += alpha * clf.predict(X_new)
        return np.sign(y_pred)
    
    return predict