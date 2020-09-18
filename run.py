import argparse
import logging
import logging.config
import sys

from src.application_db import create_db


sys.path.append('./config')
import flaskconfig
from flaskconfig import SQLALCHEMY_DATABASE_URI
import config

# Logger set up
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    # reading args for database setup
    parser = argparse.ArgumentParser(description='Database settings.')
    parser.add_argument("--truncate",
                        "-t",
                        default=False,
                        action="store_true",
                        help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
    args = parser.parse_args()

    try:
        logger.info("Selected: {}".format(SQLALCHEMY_DATABASE_URI))
        create_db(SQLALCHEMY_DATABASE_URI, args.truncate)
    except Exception as e:
        logger.error(e)
        sys.exit(1)