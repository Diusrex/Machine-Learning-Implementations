from abc import ABC, abstractmethod
from enum import Enum

class Optimizer(ABC):
    """
    Class to find local/global minimum of a cost_function.
    
    All of these will call the cost_function with differing theta values to
    move towards the minimum.
    """
    
    class Status(Enum):
        CONVERGED = 1
        OUT_OF_ITERATIONS = 2
        
    
    @abstractmethod
    def optimize(self, X, y, initial_theta, estimator_function, cost_function):
        """
        Given the data X, y and the cost_function, will attempt to find the local/global
        minimum.
        
        Will NOT change the features at all, just changes the values for theta
        
        Parameters
        --------
        X : array-like, shape [n_samples, n_features]
            Input array of features.
            
        y : array-like, shape [n_samples,]
            Input array of expected results.
            
        initial_theta : array-like, shape [n_features,]
            Starting values for theta. Array may be changed
            
        estimator_function : function
            Given X, theta should return the estimates for all n_samples in an array like object
        
        cost_function : function -> cost, gradient
            Must return [cost, gradient] given X, predicted y, and actual y
            
        Returns
        --------
        theta : array-like, shape [n_features,]
            Final values for theta.
        
        status : Optimizer.Status
            What the final status of the optimizer was - converged, out of iterations, etc.
        """
        pass
    
    @abstractmethod
    def converge_hints(self):
        """
        Returns a string containing hints for the user on how to achieve
        convergence with the used optimizer.
        """
        pass