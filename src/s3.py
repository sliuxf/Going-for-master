import os
import sys
import logging
import logging.config

import boto3

sys.path.append('./config')
import config


# AWS configuration
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Logger set up
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__file__)


def store_to_s3():
    """ Persist raw data to s3 bucket """

    try:
        # establish aws/s3 connection
        s3 = boto3.client('s3',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY
                          )
        logger.info("S3 connection established!")
    except Exception as e:
        logger.error('Fail to connect to aws s3. Please check your credentials!')
        logger.error(e)
    else:
        try:
            # upload local file to S3 bucket
            logger.info("Uploading {} to {} bucket as {}".format(config.Local_File_To_Upload,
                                                                 config.Bucket_Name,
                                                                 config.S3_Filename))
            s3.upload_file(config.Local_File_To_Upload,
                           config.Bucket_Name,
                           config.S3_Filename)
            logger.info('File successfully uploaded to S3 bucket!')
        except FileNotFoundError:
            logger.error('File not found, pleas check the file path.')
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    """ 
    The main function to persist raw data to s3 bucket, 
    and then download raw data from s3 to local
    """

    try:
        store_to_s3()
    except Exception as e:
        logger.error("Failed to persist raw data to S3 bucket!")
        logger.error(e)
