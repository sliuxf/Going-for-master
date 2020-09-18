import sys
from os import path
import pytest
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append('./src')
import clean


PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))


def test_featurize_happy():
    '''Happy path unit test for featurize(df,col)'''

    df = pd.DataFrame([0,10], columns=['cgpa'])
    col = 'cgpa'
    result_true = round(pd.DataFrame([0.0,4.0], columns=['cgpa']),1)
    result_test = clean.featurize(df, col)

    assert result_test.equals(result_true)


def test_featurize_unhappy():
    '''Unhappy path unit test for featurize(df,col)'''
    df = pd.DataFrame([0.0,0.0], columns=['cgpa'])
    col = 'cgpa'
    result_true = pd.DataFrame([0.0,0.0], columns=['cgpa'])
    result_test = clean.featurize(df, col)

    assert result_test.equals(result_true)

