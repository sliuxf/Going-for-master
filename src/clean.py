import sys
import os
import logging
import logging.config
import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import boto3
import warnings
warnings.filterwarnings('ignore')

sys.path.append('./config')
import config

# AWS configuration
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Logger Setup
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__file__)


def load_data(filename):
    """Load raw data from local

    Args:
        filename (`str`): path to local raw data

    ReturnsL
        df (`DataFrame`): dataframe contains applicants data
    """

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        logger.error("Please provide valid local file downloaded from S3")

    return df


def eda(df, fig_directory, columns):
    """Plot and save EDA plots for each features

    Args:
        df (`DataFrame`): loaded dataset
        fig_directory (`str`): directory to save figures
        columns (`list of str`): list of feature column names

    Returns:
        None
    """

    # Prepends the date to a string (e.g. to save dated files)
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    dateplus = lambda x: "%s-%s" % (now, x)

    # Construct fig directory
    os.makedirs(fig_directory, exist_ok=True)
    logger.debug("Created directory to store EDA plots: {}".format(fig_directory))

    figs = []

    # Plot distribution and save EDA for each feature
    for feat in df.columns:
        try:
            # Plot EDA for feat
            fig, ax = plt.subplots()
            ax.hist([df[feat].values])
            title = ' '.join(feat.split(' ')).capitalize()
            ax.set_ylabel('Number of observations')

            path = os.path.join(fig_directory, dateplus(title))
            fig.savefig("{}.png".format(path))
            figs.append(fig)
        except Exception as e:
            logger.warning("Failed to generate EDA plot for {}".format(feat))
            logger.warning(e)

    # construct correlation plots
    corr_fig = corr_plot(df, columns)
    title = "Correlation plot"
    path = os.path.join(fig_directory, dateplus(title))
    corr_fig.savefig("{}.png".format(path))

    plt.close()

    logger.info("Generated {} EDA plots in {}".format(len(figs), fig_directory))


def corr_plot(df, columns):
    """Helper eda function to construct correlation matrix plot

    Args:
        df (`DataFrame`): Cleaned data
        columns (`list of str`): list of feature columns names

    Return:
        fig (`matplotlib object`): Correlation plot
    """

    try:

        df = df[columns]
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(8, 8))
        colormap = sns.diverging_palette(220, 10, as_cmap=True)
        dropSelf = np.zeros_like(corr)
        dropSelf[np.triu_indices_from(dropSelf)] = True
        colormap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(corr, cmap=colormap, linewidths=.5, annot=True, fmt=".2f", mask=dropSelf)

    except Exception as e:
        logger.warning(e)

    return fig


def featurize(df, col):
    """Scale CGPA data from 0-10 to 0-4

    Args:
        df (`DataFrame`): Loaded data
        col (`str`): cgpa column name

    Return:
        df (`DataFrame`): dataframe with gpa scaled to 0-4

    """

    try:
        x = df[[col]].values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df[col] = x_scaled * 4
    except Exception as e:
        logger.error("Failed to scale GPA to 0-4 scale")
        logger.error(e)

    return df


def write_csv(df, clean_filename):
    """Write cleaned data to csv

    Args:
        df (`DataFrame`): cleaned data
        clean_filename (`str`): Path to write cleaned data

    Return:
        None

    """
    try:
        df.to_csv(clean_filename)
    except FileNotFoundError:
        logger.error("Please provide a valid file location to persist cleaned data.")


if __name__ == "__main__":
    """Clean the raw data and plot EDA"""

    load_filename = config.Path_To_Local_Raw_File

    try:
        df = load_data(load_filename)
    except Exception as e:
        logger.error("Failed to load raw data! Please check valid path")
        logger.error(e)
        sys.exit(1)

    fig_directory = config.fig_direcotry
    columns = config.Columns
    try:
        eda(df, fig_directory, columns)
        logger.info("EDA saved to {}".format(fig_directory))
    except Exception as e:
        logger.error("Failed to perform EDA.")
        logger.error(e)

    col = config.Transform_col
    try:
        df = featurize(df, col)
    except Exception as e:
        logger.error("Failed to scale gpa.")
        logger.error(e)

    clean_filename = config.Path_To_Clean_File
    try:
        write_csv(df, clean_filename)
        logger.info("Cleaned data written to {}".format(clean_filename))
    except Exception as e:
        logger.error("Failed to write cleaned data to local")
        logger.error(e)
