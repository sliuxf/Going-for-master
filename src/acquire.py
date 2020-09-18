import sys
import os
import logging
import logging.config

import boto3

sys.path.append('./config')
import config

# AWS configuration
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Logger setup
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__file__)


def pull_from_s3():
    """Pull raw data from S3 bucket"""

    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY
                          )
        logger.debug("S3 connection established!")
        s3.download_file(config.Bucket_Name, config.S3_Filename, config.Path_To_Local_Raw_File)
        logger.info('File successfully downloaded from S3 bucket!')

    except FileNotFoundError:
        logger.error('File not found, pleas check the file path.')
    except Exception as e:
        logger.error(e)



if __name__ == "__main__":
    """Pull raw data from S3 bucket"""

    try:
        pull_from_s3()
    except Exception as e:
        logger.error("Failed to pull data from S3 bucket!")
        logger.error(e)