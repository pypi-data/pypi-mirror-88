"""
Created on Thu Nov 26 17:53:34 2020.

@author: malchiodi
"""

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import skfuzzy as fuzz


class FCM(BaseEstimator, RegressorMixin):
    """Scikit-learn adapter for FCM algorithm in Scikit-fuzzy."""

    def __init__(self, m=2):
        self.m = m

    def _compute_preclustering(self, X, y):
        """Compute preclustering based on data labels."""

        return [np.array(y >= 0.5, dtype=np.float32),
                np.array(y < 0.5, dtype=np.float32)]

    def fit(self, X, y, error=0.005, maxiter=1000):
        """Fits the model."""
        X = check_array(X)

        for e in y:
            if e < 0 or e > 1:
                raise ValueError('`y` values should belong to [0, 1]')

        check_X_y(X, y)

        # Pre-allocating points in clusters using 0.5-cut of membership labels
        init = self._compute_preclustering(X, y)
        result = fuzz.cluster.cmeans(X.T, 2, self.m,
                                     error=error, maxiter=maxiter, init=init)
        self.centroids_, self.u_, _, _, _, _, _ = result

    def _compute_membership(self, X, y, error=0.001, maxiter=5000):
        """Compute the membership for generic data."""
        check_is_fitted(self, ['centroids_'])
        init = self._compute_preclustering(X, y) if y is not None else None
        result = fuzz.cluster.cmeans_predict(X.T, self.centroids_, 2,
                                             error=error, maxiter=maxiter,
                                             init=init)

        u, _, _, _, _, fpc = result
        return u, fpc

    def predict(self, X, error=0.001, maxiter=10000):
        """Predict membership of new data."""
        u, fpc = self._compute_membership(X, None, error, maxiter)
        return u.max(axis=0)

    def score(self, X, y, error=0.001, maxiter=10000):
        """Compute the score of the learnt clustering on a labeled set."""
        u, fpc = self._compute_membership(X, y, error, maxiter)
        return fpc
