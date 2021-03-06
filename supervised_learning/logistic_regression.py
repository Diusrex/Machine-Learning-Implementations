import numpy as np

# Add base directory of project to path.
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/..")

from optimization_algorithms.optimizer import Optimizer
from util.data_operation import logistic_function

class LogisticRegression(object):
    """
    Standard Logistic Regression classifier using maximum likelihood cost function.
    
    Will add a bias term to X, and otherwise not alter the data at all.
    
    Parameters
    --------
    optimizer : optimization_algorithms.Optimizer
        Will calculate the weights using the logistic function
    
    classification_boundary : numeric or None
        If provided, predict will classify samples given the boundary -
        so points with probability >= classification_boundary will be class 1,
        everything else will be class 0.
        If None, predict will return the probability of the sample being class 1.
        
    Theory
    --------
        - Highly dependent on decision boundary being linear combination of \
        provided feature set (which may not be a linear combination of original \
        feature set).
            - Decision boundary is where dot(x, theta) = 0.
        - Has low variance and high bias
            - More features it has, the more this shifts to high variance low bias.
            - To reduce overfitting it may be helpful to prune the feature set.
        - Easy to understand the effect of a single or set of features on output
            - Look at their weight. If >0, then increases likelihood, otherwise decreases
        - Just supports binary features (0 or 1).
            - To have multiple classification, create + train a LogisticRegression \
            for each class, determining how likely it is to occur. Then, for each new \
            input, class is the most likely class.
    """
    def __init__(self, optimizer, classification_boundary = None):
        self._optimizer = optimizer
        self._classification_boundary = classification_boundary
        self._weights = None
        self._intercept = None
        self._coeff = None
        
    def set_classification_boundary(self, classification_boundary):
        """
        If classification_boundary is numeric, predict will classify samples
        given the boundary - so points with
        probability >= classification_boundary will be class 1,
        everything else will be class 0.
        If classification_boundary is None, predict will return the probability
        of the sample being class 1.
        """
        self._classification_boundary = classification_boundary
        
    def fit(self, X, y):
        """
        Fit internal parameters to minimize MSE on given X y dataset.
        
        Will add a bias term to X.
        
        Parameters
        ---------
        
        X : array-like, shape [n_samples, n_features]
            Input array of features.
            
        y : array-like, shape [n_samples,] or [n_samples,n_values]
            Input array of expected results. Must be binary (0 or 1)
        """
        # Add bias columns as first column
        X = np.insert(X, 0, 1, axis=1)
        
        num_features = np.shape(X)[1]
        self._weights = np.zeros((num_features, ))
        self._weights, status = self._optimizer.optimize(
                X, y,
                self._weights,
                LogisticRegression._cost_function)

        if (status != Optimizer.Status.CONVERGED):
            print("WARNING: Optimizer did not converge:", self._optimizer.converge_hints())
        
        self._intercept = self._weights[0]
        self._coeff = self._weights[1:]
        
    def predict(self, X):
        """
        Predict the value(s) associated with each row in X.
        
        X must have the same size for n_features as the input this instance was
        trained on.
        
        Parameters
        ---------
        
        X : array-like, shape [n_samples, n_features]
            Input array of features.
            
        Returns
        ---------
        Values in range [0, 1] indicating how sure the predictor is that a value
        is 1. To choose most likely, use np.round.
        """
        X = np.insert(X, 0, 1, axis=1)
        values = LogisticRegression._logistic_function(X, self._weights)
        if self._classification_boundary is None:
            return values
        
        return values >= self._classification_boundary
    
    def classification_weight(self, X):
        """
        Rill return a weight in range -inf to inf of how sure the ML algorithm
        is that the sample was class 1 (positive) or class 0 (negative).
        
        Parameters
        ---------
        
        X : array-like, shape [n_samples, n_features]
            Input array of features.
            
        Returns
        ---------
        Values ranging from -inf to +inf. If a sample is negative, would be classified
        as class 0, and positive means would be classified as class 1. The greater the
        magnitude, the more confident the ml would be.
        """
        X = np.insert(X, 0, 1, axis=1)
        return np.dot(X, self._weights)
    
    def _logistic_function(X, theta):
        value = np.dot(X, theta)
        return logistic_function(value)
    
    def _cost_function(X, theta, y):
        """
        Cost using maximum likelihood.
        """
        pred = LogisticRegression._logistic_function(X, theta)
        
        m = len(y)
        # TODO: Refactor this into a cost + gradient function in data_operation?
        cost = 1/m * (-np.dot(y.T, np.log(pred)) - np.dot((1-y), np.log(1-pred)))
        gradient = 1/m * np.dot(X.T, (pred - y))
        return (cost, gradient)
        
    def get_feature_params(self):
        return self._coeff
