import sys
import logging
import logging.config
import warnings
warnings.filterwarnings('ignore')

import sklearn
from sklearn import model_selection
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
import pandas as pd
import numpy as np

sys.path.append('./config')
import config


# Logger setup
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__file__)


def load_data(clean_location):
    """Load cleaned feautres and target data from local, and do train test split

    Args:
        clean_location (`str`): path to cleaned data

    Returns:
        df (`DataFrame`): loaded data

    """

    # Load data
    try:
        df = pd.read_csv(clean_location)

        logger.info("Successfully loaded features and target data!")
    except FileNotFoundError:
        logger.error("Please provide valid feature and target csv path")

    return df


def split(df, columns, target, split_params):
    """Do train test split

    Args:
        df (`DataFrame`): loaded data
        columns (`list of str`): list of feature column names
        target (`str`): target colume name
        split_params (`dict`): parameters for train test split

    Returns:
        X_train (`DataFrame`): features of training set
        X_test (`DataFrame`): features of test set
        y_train (`Series`): target of training set
        y_test (`Series`): target of test set
    """
    try:
        # Train test split
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            df[columns], df[target], test_size=split_params['test_size'],
            random_state=split_params['random_state'])

        logger.info("Train test split with test size = {} and random state = {}"
                    .format(split_params['test_size'], split_params['random_state']))

        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(e)
        return "Failed to train test split"


def cv_linear(X_train, y_train, model_params):
    """ K-folds Cross Validation of Linear Regressinon

    Args:
        X_train (`DataFrame`): Training set features
        y_train (`Series`): Training set target
        model_params (`dict`): Stores model hyperparameters

    Return:
        linear_peform (`list of float`): model performance metrics for CV

    """

    try:
        lr = LinearRegression()
        cv = ShuffleSplit(n_splits=model_params['cv'],
                          test_size=model_params['test_size'],
                          random_state=model_params['random_state'])
        linear_peform = cross_val_score(lr, X_train, y_train,
                                        scoring=model_params['scoring'], cv=cv)
        logger.debug("Trained linear regression of random state = {} and CV = {}"
                     .format(model_params['random_state'],
                             model_params['cv']))
        return linear_peform
    except Exception as e:
        logger.error("Failed to CV linear regression")
        logger.error(e)
        return "Failed cv_linear"


def cv_lasso(X_train, y_train, model_params):
    """ K-folds Cross Validation of Lasso Regressinon

    Args:
        X_train (`DataFrame`): Training set features
        y_train (`Series`): Training set target
        model_params (`dict`): Stores model hyperparameters

    Return:
        lasso_peform (`list of float`): model performance metrics for CV

    """

    try:
        lasso = Lasso()
        cv = ShuffleSplit(n_splits=model_params['cv'],
                          test_size=model_params['test_size'],
                          random_state=model_params['random_state'])
        lasso_peform = cross_val_score(lasso, X_train, y_train,
                                       scoring=model_params['scoring'], cv=cv)
        logger.debug("Trained lasso regression of random state = {} and CV = {}"
                     .format(model_params['random_state'],
                      model_params['cv']))
        return lasso_peform
    except Exception as e:
        logger.error("Failed to CV Lasso regression")
        logger.error(e)
        return "Failed cv_lasso"


def cv_rf(X_train, y_train, model_params):
    """ K-folds Cross Validation of Random Forest

    Args:
        X_train (`DataFrame`): Training set features
        y_train (`Series`): Training set target
        model_params (`dict`): Stores model hyperparameters

    Return:
        rf_peform (`list of float`): model performance metrics for CV

    """

    try:
        rf = RandomForestRegressor(random_state=model_params['random_state'])
        cv = ShuffleSplit(n_splits=model_params['cv'],
                          test_size=model_params['test_size'],
                          random_state=model_params['random_state'])
        rf_peform = cross_val_score(rf, X_train, y_train,
                                    scoring=model_params['scoring'], cv=cv)
        logger.debug("Trained random forest of random state = {} and CV = {}".
                     format(model_params['random_state'], model_params['cv']))
        return rf_peform
    except Exception as e:
        logger.error("Failed to CV Random Forest")
        logger.error(e)
        return "Failed cv_rf"


def write_models_perform(r2, rmse, perform_path):
    """Write model performance to csv

    Args:
        r2 (`list of float64`): list of r2 metric for three models
        rmse (`list of float64`): list of rmse metric for three models
        perform_path (`str`): path to save model performance

    """

    try:
        pd.DataFrame({'r2':r2, 'rmse':rmse}, index = ['linear','lasso','rf'])\
            .to_csv(perform_path)
        logger.info("Model performance metrics written to {}".format(perform_path))
    except FileNotFoundError:
        logger.error("Check valid model performance path")
    except Exception as e:
        logger.error("Failed to write model performance to file")
        logger.error(e)


if __name__ == "__main__":
    """Prepare, train, and evaluate the model to predict chance of admit"""

    clean_location = config.Path_To_Clean_File
    columns = config.Columns
    target = config.Target
    split_params = config.split_params

    try:
        # Load data and perform train test split
        df = load_data(clean_location)
        X_train, X_test, y_train, y_test = split(df, columns, target, split_params)
    except FileNotFoundError:
        logger.error("Please provide valid features and target file path")
        sys.exit(1)
    except Exception as e:
        logger.error("Failed to load and split the data into train and test sets")
        logger.error(e)
        sys.exit(1)

    try:
        # calculate rmse
        model_params = config.model_params_rmse
        linear = cv_linear(X_train, y_train, model_params)
        lasso = cv_lasso(X_train, y_train, model_params)
        rf = cv_rf(X_train, y_train, model_params)

        rmse = [np.mean(np.sqrt(-1 * (linear))),
                np.mean(np.sqrt(-1 * (lasso))),
                np.mean(np.sqrt(-1 * (rf)))]

        # calculate r2
        model_params = config.model_params_r2
        linear = cv_linear(X_train, y_train, model_params)
        lasso = cv_lasso(X_train, y_train, model_params)
        rf = cv_rf(X_train, y_train, model_params)

        r2 = [np.mean(linear),
              np.mean(lasso),
              np.mean(rf)]
    except Exception as e:
        logger.error("Failed to train the model.")
        logger.error(e)
        sys.exit(1)

    perform_path = config.Selection_Perform_Path
    try:
        write_models_perform(r2, rmse, perform_path)
    except FileNotFoundError:
        logger.error("Please check valid model performance path!")
