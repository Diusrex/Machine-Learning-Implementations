import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets


# Add base directory of project to path.
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../..")

from util.data_operation import accuracy, mean_square_error
from util.data_manipulation import train_test_split

from supervised_learning.logistic_regression_tf import LogisticRegressionTF

def main(_=None):
    # Just has one feature to make it easy to graph.
    X, y = datasets.make_classification(n_samples=200, n_features=1, n_informative=1, n_redundant=0,
                                        n_clusters_per_class=1, flip_y=0.1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_proportion=0.2)
    
    logistic_reg = LogisticRegressionTF()
    logistic_reg.fit(X_train, y_train)
    
    y_pred_probability = logistic_reg.predict(X_test)
    y_pred_probability = np.squeeze(y_pred_probability)
    mse = mean_square_error(y_pred_probability, y_test)
    
    logistic_reg.set_classification_boundary(0.5)
    y_pred_classified = logistic_reg.predict(X_test)
    y_pred_classified = np.squeeze(y_pred_classified)
    acc = accuracy(y_pred_classified, y_test)
    
    plt.figure()
    plt.scatter(X_test, y_test, color="Black", label="Actual")
    plt.scatter(X_test, y_pred_probability, color="Red", label="Classification Probability")
    plt.scatter(X_test, y_pred_classified, color="Blue", label="Rounded Prediction")
    plt.legend(loc='center right', fontsize=8)
    plt.title("Logistic Regression %.2f MSE, %.2f%% Accuracy)" % (mse, acc*100))
    plt.show()

if __name__ == "__main__":
    tf.app.run()
