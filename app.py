import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Tracks
from flask import Flask
from src.application_db import Applications
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd


# Initialize the Flask application
app = Flask(__name__, template_folder="./app/templates", static_folder="./app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Main view that takes user input and make predictions.

    Create view into index page that uses data queried from Application database and
    inserts it into the app/templates/index.html template.

    Returns:
        rendered html template: when request.method == 'GET'
        redirect '/': when request.method == 'POST'

    """

    if request.method == 'POST':

        try:
            # get user input
            gre = float(request.form['gre'])
            toefl = float(request.form['toefl'])
            univ_rating = float(request.form['univ_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            gpa = float(request.form['gpa'])
            research = float(request.form['research'])

            # Make prediction
            file = pd.read_csv('./models/final model.csv')
            newx = pd.Series([1, gre, toefl, univ_rating, sop, lor, gpa, research])
            pred = round(float(file.coefs.dot(newx)), 2)

            # Ensure prediction is in range [0,1]
            if pred > 1:
                pred = 1
            elif pred < 0:
                pred = 0

            # add record to database
            app = Applications(gre=gre, toefl=toefl, univ_rating=univ_rating,
                               sop=sop, lor=lor, cgpa=gpa, research=research,
                               admit=pred)
            db.session.add(app)
            db.session.commit()
            logger.debug("application successfully added to database")
            return redirect('/')
        except ValueError:
            logger.warning("Please input valid application record")
            return redirect('/')
        except Exception as e:
            logger.warning("Not able to add application to database, error page returned")
            logger.error(e)
            return render_template('error.html')
    else:
        try:

            # Query the latest added application from database
            app = db.session.query(Applications).order_by(Applications.id.desc()).first()
            logger.info("queried latest record from database")
            return render_template('index.html', pred=app)

        except Exception as e:
            logger.warning("Not able to query application prediction, error page returned")
            logger.error(e)
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
