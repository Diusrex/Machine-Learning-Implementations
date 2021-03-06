# Add base directory of project to path.
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../..")

from util.data_operation import accuracy
from util.data_manipulation import train_test_split
from util.data_generation import create_linearly_separable_two_class
from util.graphing import class_estimation_graph

from supervised_learning.svm import SVM, Kernel, svm_able_to_run

from sklearn import datasets

def linearly_separable():
    X, y = create_linearly_separable_two_class()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_proportion=0.2)
    classifier = SVM(Kernel.linear_kernel())
    classifier.fit(X_train, y_train)
    
    y_pred = classifier.predict(X_test)
    acc = accuracy(y_pred, y_test)
    
    class_estimation_graph(2, X_test, y_test, y_pred,
                           "SVM linear %.2f%% Accuracy on Linearly Separable.\nShape is true class, color is estimate" % (acc*100))

def with_data_error_force_accurate():
    n_classes = 2
    # Just has one feature to make it easy to graph.
    X, y = datasets.make_classification(n_samples=200, n_features=2, n_informative=2, n_redundant=0,
                                        n_clusters_per_class=1, flip_y=0.1, n_classes=n_classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_proportion=0.2)
    classifier = SVM(Kernel.linear_kernel())
    
    try:
        classifier.fit(X_train, y_train)
        raise RuntimeError("Should not have successfully fit the model")
    except AssertionError as e:
        # We expect an AssertionError since the problem is non-separaable.
        pass

def with_data_error_with_slack():
    n_classes = 2
    # Just has one feature to make it easy to graph.
    X, y = datasets.make_classification(n_samples=200, n_features=2, n_informative=2, n_redundant=0,
                                        n_clusters_per_class=1, flip_y=0.1, n_classes=n_classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_proportion=0.2)
    classifier = SVM(Kernel.linear_kernel(), C=1)
    classifier.fit(X_train, y_train)
    
    
    y_pred = classifier.predict(X_test)
    acc = accuracy(y_pred, y_test)
    
    class_estimation_graph(n_classes, X_test, y_test, y_pred,
                           "SVM linear %.2f%% Accuracy.\nShape is true class, color is estimate" % (acc*100))
    
def main():
    if svm_able_to_run:
        linearly_separable()
        
        with_data_error_force_accurate()
        
        with_data_error_with_slack()
    else:
        print("WARNING: cvxopt not installed, SVM will not work.")

if __name__ == "__main__":
    main()
