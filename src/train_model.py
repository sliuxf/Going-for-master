import sys
import os
import logging
import logging.config
import warnings
warnings.filterwarnings('ignore')

import sklearn
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

sys.path.append('./config')
import config


# Logger Setup
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


def train_model(X_train, y_train):
    """Train the logistic regression model using the training set

    Args:
        X_train (`DataFrame`): features of training set
        y_train (`Series`): target of training set

    Returns:
        lr (`TMO`): trained linear regression model object
    """

    # Set up regressor
    lr = LinearRegression()

    try:
        # Fit a linear regression model
        lr.fit(X_train, y_train)
        logger.debug("Fitted a linear regression!")
        return lr
    except ValueError:
        logger.error("Features have to be numerical.")
        return "Failed train_model"


def feature_importance(X_train, y_train, fig_directory, feature_plot_path, random_state):
    """Find feature importance by ranfom forest and save figure to local

    Args:
        X_train (`DataFrame`): features of training set
        y_train (`Series`): target of training set
        fig_directory (`str`): directory to save figures
        feature_plot_path (`str`): name of feature importance plot
        random_state (`int`): random state for random forest

    Return:
        None
    """
    try:
        classifier = RandomForestRegressor(random_state=random_state)
        classifier.fit(X_train, y_train)
        feature_names = X_train.columns
        importance_frame = pd.DataFrame()
        importance_frame['Features'] = X_train.columns
        importance_frame['Importance'] = classifier.feature_importances_
        importance_frame = importance_frame.sort_values(by=['Importance'],
                                                        ascending=True)
        fig = plt.figure(figsize=(12,8))
        plt.barh([1, 2, 3, 4, 5, 6, 7], importance_frame['Importance'],
                 align='center', alpha=0.5)
        plt.yticks([1, 2, 3, 4, 5, 6, 7], importance_frame['Features'])
        plt.xlabel('Importance')
        plt.title('Feature Importances')
        path = os.path.join(fig_directory, feature_plot_path)
        fig.savefig(path)
        logger.info("Feature importance plot saved!")
    except Exception as e:
        logger.error("Failed save feature importance plot by random forest")
        logger.error(e)


def model_performance(lr, X_test, y_test, model_eval_path):
    """Evaluate model performance and write performance metrics to files

    Args:
        lr (`TMO`): trained logistic regression model object
        X_test (`DataFrame`): features of test set
        y_test (`Series`): target of test set
        model_eval_path (`str`): path to write model performance metrics

    Returns:
        None
    """

    try:
        # Check model performance
        ypred = lr.predict(X_test)
        r2 = metrics.r2_score(y_test, ypred)
        rmse = np.sqrt(metrics.mean_squared_error(y_test, ypred))
        logger.debug("Evaluated model by r2 and rmse")
    except Exception as e:
        logger.error("Failed to evaluate model performance")
        logger.error(e)

    try:
        # Write performance to csv
        pd.DataFrame({'r2': [r2], 'rmse': [rmse]})\
            .to_csv(model_eval_path)
    except FileNotFoundError:
        logger.error("Please check for valid final model performance path")


def save_model(lr, initial_features, csv_path, pickle_path):
    """Save trained final model

    Args:
        lr (`TMO`): trained logistic regression model object
        initial_features  (`list of str`): list of feature names
        csv_path  (`str`): path to write model coefficients to csv
        pickle_path (`str`): path to write TMO to pickle file
    """

    try:
        fitted = pd.DataFrame([])
        fitted['params'] = ['intercept'] + initial_features
        fitted['coefs'] = np.append(lr.intercept_, lr.coef_)

        # Persist to csv
        fitted.to_csv(csv_path)
        logger.info("Successfully written model to {}".format(csv_path))

        # Persist to pickle
        if pickle_path is not None:
            with open(pickle_path, "wb") as f:
                pickle.dump(lr, f)
            logger.info("Trained model object saved to %s", pickle_path)

    except FileNotFoundError:
        logger.error("Please provide valid location to store model")


if __name__ == "__main__":
    """Prepare, train, and evaluate the model to classify clouds"""

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

    lr = train_model(X_train, y_train)

    try:
        model_eval_path = config.Final_Mode_Eval_Path
        model_performance(lr, X_test, y_test, model_eval_path)

        fig_directory = config.fig_direcotry
        feature_plot_path = config.Feature_Plot_Name
        random_state = config.Random_state
        feature_importance(X_train, y_train, fig_directory,
                           feature_plot_path, random_state)
    except Exception as e:
        logger.error("Failed to evaluate final model performance and feature importance")
        logger.error(e)
        sys.exit(1)

    csv_path = config.Model_CSV_Path
    pickle_path = config.Model_Pickle_Path
    try:
        save_model(lr, columns, csv_path, pickle_path)
    except Exception as e:
        logger.error("Failed to persist final models")
        logger.error(e)
