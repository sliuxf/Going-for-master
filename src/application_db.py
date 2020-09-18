import logging
import logging.config
import os
import sys
import argparse

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlite3

sys.path.append('./config')
import config


# Logger set up
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Database set up
conn_type = config.MYSQL_CONN_TYPE
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")
rds_engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
sqlalchemy_engine_string = config.SQLALCHEMY_ENGINE_STRING
#data_path = config.LOCAL_FILE_PATH # unused, for reading data in the future


Base = declarative_base()

class Applications(Base):
    """Create a data model for the database to be set up for capturing applications
    """

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    gre = Column(Integer, unique=False, nullable = False)
    toefl = Column(Integer, unique=False, nullable = False)
    univ_rating = Column(Integer, unique=False, nullable = False)
    sop = Column(String(100), unique=False, nullable = False)
    lor = Column(String(100), unique=False, nullable = False)
    cgpa = Column(String(100), unique=False, nullable = False)
    research = Column(Integer, unique=False, nullable = False)
    admit = Column(String(100), unique=False, nullable = False)

    def __repr__(self):
        return '<Serial Number %r>' % self.id


def _truncate_applications(session):
    """Deletes tweet scores table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM applications''')



def create_db(engine_string, truncate):
    """Persist data to selected database
    Args:
        engine_string (`str`): the user-selected database engine string
        truncate (`boolean`): boolean indicates whether to truncate the application table
    """

    try:
        # set up mysql connection
        engine = sql.create_engine(engine_string)

        # create the application table
        Base.metadata.create_all(engine)

        # create a db session
        Session = sessionmaker(bind=engine)
        session = Session()

    except Exception as e:
        logger.error("Failed in db connection.")
        logger.error(e)
        #sys.exit(1)

    try:
        # create a db session
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        logger.error("Failed in db connection.")
        logger.error(e)
        sys.exit(1)


    # Truncate application table
    if truncate:
        try:
            logger.debug("Attempting to truncate application table.")
            _truncate_applications(session)
            session.commit()
            logger.info("applications truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate application table.")
            logger.error(e)
            sys.exit(1)

    session.close()



