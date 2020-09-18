import sys
from os import path
import pytest
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append('./src')
import model_selection


PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
data = [[1,2,3,4],[2,2,3,4],[3,2,3,4], [4,2,3,4]]
cols = ['a', 'b', 'c', 'd']
target = 'd'
features = ['a','b','c']
xtrain = [[4,2,3],[3,2,3],[1,2,3]]
xtest = [[2,2,3]]
ytrain = [4,4,4]
ytest = [4]


def test_split_happy():
    '''Happy path unit test for split(df, columns, target, split_params)'''

    df = pd.DataFrame(data, columns=cols)
    split_params = {"test_size": 0.25,
                    "random_state": 1995
                    }
    result_true = np.array([4])
    _, _, _, result_test = model_selection.split(df, cols, target, split_params)

    assert all(result_test.values == result_true)



def test_split_unhappy():
    '''Unhappy path unit test for split(df, columns, target, split_params)'''

    df = pd.DataFrame([], columns=cols)
    split_params = {"test_size": 0.25,
                    "random_state": 1995
                    }
    result_true = "Failed to train test split"
    result_test = model_selection.split(df, cols, target, split_params)

    assert result_test == result_true


def test_cv_linear_happy():
    '''Happy path for cv_linear(X_train, y_train, model_params)'''
    x_train = pd.DataFrame(xtrain, columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = np.array([-0.,-0.,-0.])
    result_test = model_selection.cv_linear(x_train,y_train,model_params_rmse)

    assert np.array_equal(result_true,result_test)


def test_cv_linear_happy():
    '''Happy path for cv_linear(X_train, y_train, model_params)'''
    x_train = pd.DataFrame(xtrain, columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = np.array([-0.,-0.,-0.])
    result_test = model_selection.cv_linear(x_train,y_train,model_params_rmse)

    assert np.array_equal(result_true,result_test)


def test_cv_linear_unhappy():
    '''Unhappy path for cv_linear(X_train, y_train, model_params)'''
    x_train = pd.DataFrame([], columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = "Failed cv_linear"
    result_test = model_selection.cv_linear(x_train,y_train,model_params_rmse)

    assert result_true == result_test


def test_cv_lasso_happy():
    '''Happy path for cv_lasso(X_train, y_train, model_params)'''
    x_train = pd.DataFrame(xtrain, columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = np.array([-0.,-0.,-0.])
    result_test = model_selection.cv_lasso(x_train,y_train,model_params_rmse)

    assert np.array_equal(result_true,result_test)


def test_cv_lasso_unhappy():
    '''Unhappy path for cv_lasso(X_train, y_train, model_params)'''
    x_train = pd.DataFrame([], columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = "Failed cv_lasso"
    result_test = model_selection.cv_lasso(x_train,y_train,model_params_rmse)

    assert result_true == result_test


def test_cv_rf_happy():
    '''Happy path for cv_rf(X_train, y_train, model_params)'''
    x_train = pd.DataFrame(xtrain, columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = np.array([-0.,-0.,-0.])
    result_test = model_selection.cv_rf(x_train,y_train,model_params_rmse)

    assert np.array_equal(result_true,result_test)


def test_cv_rf_unhappy():
    '''Unhappy path for cv_rf(X_train, y_train, model_params)'''
    x_train = pd.DataFrame([], columns=features)
    y_train = pd.DataFrame({'d': [4, 4, 4]})
    model_params_rmse = {"scoring": 'neg_mean_squared_error',
                         'random_state': 1995,
                         "test_size": 0.25,
                         "cv": 3
                         }
    result_true = "Failed cv_rf"
    result_test = model_selection.cv_rf(x_train,y_train,model_params_rmse)

    assert result_true == result_test