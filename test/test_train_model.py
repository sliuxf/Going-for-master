import sys
from os import path
import pytest
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append('./src')
import train_model


PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
data = [[1,2,3,4],[2,2,3,4],[3,2,3,4], [4,2,3,4]]
cols = ['a', 'b', 'c', 'd']
target = 'd'


def test_split_happy():
    '''Happy path unit test for split(df, columns, target, split_params)'''

    df = pd.DataFrame(data, columns=cols)
    split_params = {"test_size": 0.25,
                    "random_state": 1995
                    }
    result_true = np.array([4])
    _, _, _, result_test = train_model.split(df, cols, target, split_params)

    assert all(result_test.values == result_true)



def test_split_unhappy():
    '''Unhappy path unit test for split(df, columns, target, split_params)'''

    df = pd.DataFrame([], columns=cols)
    split_params = {"test_size": 0.25,
                    "random_state": 1995
                    }
    result_true = "Failed to train test split"
    result_test = train_model.split(df, cols, target, split_params)

    assert result_test == result_true


def test_train_model_happy():
    '''Happy path unit test for train_model(X_train, y_train)'''

    X_train = [[2, 4, 6, 8], [2, 4, 6, 8], [2, 4, 6, 8], [2, 4, 6, 8]]
    y_train = [1, 2, 3, 4]
    lr_test = train_model.train_model(X_train, y_train)
    result_test = lr_test.coef_
    result_true = np.array([0.,0.,0.,0.])

    assert (result_true == result_test).all()


def test_train_model_unhappy():
    """Unhappy path unit test for train_model(X_train, y_train)"""

    X_train = [[2, 4, 6, 8], [2, 4, 6, 8], [2, 4, 6, 8], [2, 4, 6, 8]]
    y_train = []
    result_test = train_model.train_model(X_train, y_train)
    result_true = "Failed train_model"

    assert result_true == result_test

