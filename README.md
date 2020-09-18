# MSiA423 Course Project: Going For Masters? Graduate Admission Prediction

####Project by Xuefei (Shirley) Liu, QA by Duyun (Ellie) Tan



<!-- toc -->
- [Project Charter](#project-charter)
- [Sprint Planning](#sprint-planning)
  * [Initiative 1: Development of methods for predicting admission outcome and drawing insights](#initiative-1-development-of-methods-for-predicting-admission-outcome-and-drawing-insights)
  * [Initiative 2: Build fully reproducible web application for interactive usage](#initiative-2-build-fully-reproducible-web-application-for-interactive-usage)
  * [Initiative 3: Web app deployment](#initiative-3-web-app-deployment)
- [Backlog](#backlog)
- [Icebox](#icebox)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [Download raw data from Kaggle](#initialize-the-database)
  * [Setting up](#Setting-up)
    + [0. Log in Northwestern VPN and stay connected through the entire process](#0-Log-in-Northwestern-VPN-and-stay-connected-through-the-entire-process)
    + [1. Set up environment](#1-Set-up-environment)
    + [2. Set up configurations](#2-Set-up-configurations)
  * [Building the docker image and running Machine Learning Model Pipeline](#Building-the-docker-image-and-running-Machine-Learning-Model-Pipeline)
    + [1. Build the docker image](#1-Build-the-docker-image)
    + [2. Execute the pipeline](#2-Execute-the-pipeline)
    + [3. Run Reproducibility tests](#3-Run-Reproducibility-tests)
  * [Deploying Local Web application](#Deploying-Local-Web-application)
    + [1. Build the docker image](#1-Build-the-docker-image)
    + [2. Run the container](#2-run-the-container)
    + [3.Kill the container](#3-kill-the-container)
    


<!-- tocstop -->

## Project Charter

**Vision**

The predicted admission decision can help prospective students better understand where they stand in all applicants. 
Based on the predictions, they can form smarter application strategies and decide the school list to apply to.

The predicted admission decision is also beneficial to graduate program admission officers. 
They can use the predicted results to select competitive applications instead of going through all applications. 
The admission process will be more efficient.


**Mission**

The graduate admission web app will provide a user interactive approach to predict admission outcome. 
The users can input important factors for a Master Program application (eg, GRE, GPA). A machine model 
will be pre-trained and tested by the Graduate Admission 2 dataset on Kaggle provided by Mohan S Acharya 
on Kaggle. (https://www.kaggle.com/mohansacharya/graduate-admissions) In terms of admission outcome, either 
a yes/no admission result or a chance of admission will be the output. Along with the results, insightful 
explanatory analysis will also be provided for users to better understand their application status.

**Success Criteria**
* *Business criteria*: 
	* Number of daily(or weekly) active users (5 users)
	* Average time per active user per session (2 minutes)
	* Average number of predictions per active user per session (1 prediction)
	* Fraction of users retained (30%)
* *Model Performance Criteria*
	* MSE (0.3)
	* R-squared (0.6)


## Sprint Planning  
### Initiative 1: Development of methods for predicting admission outcome and drawing insights
* **Epic 1: Draw insights from EDA**
	* Story 1: Data preprocessing. Check for missing values, class imbalance, model assumptions, etc
	* Story 2: Visualize data . Check for model assumptions 
	* Story 3: Feature engineering and data transformation if necessary
* **Epic 2: Draw insights from EDA**
	* Story 1: Build a baseline model 
	* Story 2: Perform k-fold cross validation to tune hyper-parameters for other models. 
	(Regularization/trees, etc)
	* Story 3: Convert numerical outcome from regression models (chance of admission) into binary outcome 
	(whether admitted or not)
	* Story 4: Compare machine learning model performance criteria, and select the best model
 
### Initiative 2: Build fully reproducible web application for interactive usage
* **Epic 1: A running RDS instance with tables used by the web app**
* **Epic 2: An S3 bucket to storing raw source data**
* **Epic 3: Build a web app (Flask) that can be deployed locally on a computer using Docker**
	 * Story 1: A requirements file that covers all necessary Python dependencies
	 * Story 2: Front-end construction and design
	 * Story 3: Prepare reproducible test 
	 * Story 4: Proper configuration management 
	 * Story 5: Check for adequate code readability/documentation/Docstrings

### Initiative 3: Web app deployment
* **Epic 1: Web app pre-deployment**
	 * Story 1: Prepare unit tests where appropriate with proper documentation as how to run the tests
	 * Story 2: Check business success criteria
	 * Story 3: Demo demonstration
* **Epic 2: Web app deployment**


## Backlog
1. Initiative1.Epic1.Story1 (1 point) - FINISHED
2. Initiative1.Epic1.Story2 (2 points) - FINISHED
3. Initiative1.Epic1.Story3 (1 point) - FINISHED
4. Initiative1.Epic2.Story1 (1 point) - FINISHED
5. Initiative1.Epic2.Story2 (4 points) - FINISHED
6. Initiative1.Epic2.Story3 (2 points) - FINISHED
7. Initiative1.Epic2.Story4 (2 points) - FINISHED
8. Initiative2.Epic3.Story1 (1 point) - FINISHED
9. Initiative2.Epic3.Story2 (4 points) - FINISHED
10. Initiative2.Epic3.Story3 (2 points) - FINISHED
11. Initiative2.Epic3.Story4 (1 point) - FINISHED


## Icebox
- Initiative2.Epic1 - FINISHED
- Initiative2.Epic2 - FINISHED
- Initiative2.Epic3.Story5 - FINISHED
- Initiative3.Epic1.Story1 - FINISHED
- Initiative3.Epic1.Story2 - FINISHED
- Initiative3.Epic1.Story3 - FINISHED
- Initiative3.Epic2 - FINISHED



##






## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── logging/                      <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   │   ├── local.conf                <- Configuration of python loggers
│   ├── config.py                     <- Configurations for data science pipeline
│   ├── flaskconfig.py                <- Configurations for Flask API 
│   ├── s3.env                        <- Credential configurations for S3 bucket 
│   ├── mysql.env                     <- Credential configurations for RDS 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests 
│
├── app.py                            <- Flask wrapper for running the model 
├── Dockerfile                        <- Dockerfile for building image to run .py files
├── Dockerfile_bash                   <- Dockerfile for running the model pipeline
├── README.md                         <- README contains instruction of this repository
├── requirements.txt                  <- Python package dependencies 
├── run.py                            <- Simplifies the execution of database management of the src scripts 
├── run-pipeline.sh                   <- bash script to run the model pipeline
├── run-reproducibility-tests.sh      <- bash script to run model reproducibility tests

```


## Running the app

### Download raw data from Kaggle
Navigate to https://www.kaggle.com/mohansacharya/graduate-admissions to download the 
raw data. There are two csv files in the downloaded `graduate-admission` folder. Move `Admission_Predict_Ver1.1.csv` to 
`./data` directory.

### Setting up
#### 0. Log in Northwestern VPN and stay connected through the entire process
#### 1. Set up environment
Navigate to the root directory of this project, then:
```bash
cd config
vi s3.env
```
Open `s3.env` to edit user S3 credentials:
```bash
AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
```

Then open `mysql.env` to edit RDS credentials:
```bash
vi mysql.env
```
Fill in the following credentials:
```bash
MYSQL_USER=<YOUR_USERNAME>
MYSQL_PASSWORD=<YOUR_PASSWORD>
MYSQL_HOST=<YOUR_HOST>
MYSQL_PORT=3306
DATABASE_NAME=<YOUR_DATABASE_NAME>
```
By default, `MYSQL_PORT=3306` because this project uses MySQL database.


#### 2. Set up configurations
Stay in the `./config` directory. Edit configurations by:
```bash
vi config.py
```

Set up the following for S3 bucket: 
```bash
Bucket_Name = 'YOUR BUCKET NAME'
S3_Filename = 'admission.csv'
Local_File_To_Upload = './data/Admission_Predict_Ver1.1.csv'
```
Change `Local_File_To_Upload` if user uses another file directory.

Change `S3_Filename` if user wants to save the file as another name on S3.

The local SQLite database is set up by:
```bash
MYSQL_CONN_TYPE = 'mysql+pymysql'
LOCAL_FILE_PATH='./data/Admission_Predict_Ver1.1.csv'
DATABASE_PATH = '/app/data/application.db'
SQLALCHEMY_ENGINE_STRING = 'sqlite:////{}'.format(DATABASE_PATH)
```
Users can change to fit their own needs of database usages.

### Building the docker image and running Machine Learning Model Pipeline
Set up is completed. Make sure user has uploaded raw data file into their S3 bucket. 

#### 1. Build the docker image
Now navigate to the root directory of this project to build the docker image for executing pipeline:
```bash
cd ..
docker build -f Dockerfile_bash -t application-pipeline .
```
#### 2. Execute the pipeline
Run the pipeline to acquire - clean - featurize the data, and then fit and evaluate a model
```bash
docker run --env-file=./config/s3.env --mount type=bind,source="$(pwd)"/,target=/app/ application-pipeline run-pipeline.sh
``` 

If raw data is not in S3 bucket yet, open `vi run-pipeline.sh` and add `python3 ./src/s3.py` at the beginning

#### 3. Run Reproducibility tests
Then, run reproducibility tests for model pipeline
```bash
docker run --mount type=bind,source="$(pwd)"/,target=/app/ application-pipeline run-reproducibility-tests.sh
```

### Deploying Local Web application

#### 1. Build the docker image
In the root directory:
```bash
docker build -f app/Dockerfile -t application_webapp .  
```

#### 2. Run the container
The users can choose to connect the web app to a RDS or local sqlite database by simply specifying the environment 
variables.

* Notice: Before launching the web app, users will have to first create their own database, which is done by: 
`run.py` in `./app/boot.sh` in the following `docker run` command.  

If user want to deploy the model with a local sqlite database:
```bash
docker run --mount type=bind,source="$(pwd)"/,target=/app/ -p 5000:5000 --name testsl -t -i application_webapp 
```
If user want to deploy the model with RDS database, make sure users have configured mysql.env described in step 2 
in Setting Up:
```bash
docker run --env-file=./config/mysql.env --mount type=bind,source="$(pwd)"/,target=/app/ -p 5000:5000 --name testsl -t -i application_webapp 
```

Users should now be able to access the app at http://0.0.0.0:5000/ in the browser.

This command runs the `application_webapp` image as a container named `testsl` and forwards the port 5000 from 
container to laptop so that users can access the flask app exposed through that port.


Users can go to `./config/flaskconfig.py` to configure flask app, database engine strings, etc.

If users want to truncate the database before launching the app, they can go to `./app/boot.sh` and 
change `python3 run.py` to `python3 run.py -t`

#### 3. Kill the container
When users finish exploring the web application, `Ctrl+C` to exit. Then:
```bash
docker container rm /testsl
```
