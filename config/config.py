from os import path

# Logging
LOGGING_CONFIG = './config/logging/local.conf'

# S3 config
Bucket_Name = 'msia-sliuxf-avc-project'
S3_Filename = 'admission.csv'
Local_File_To_Upload = './data/Admission_Predict_Ver1.1.csv'
Path_To_Local_Raw_File = './data/admission.csv'

# Database config
MYSQL_CONN_TYPE = 'mysql+pymysql'
DATABASE_PATH = '/app/data/application.db'
SQLALCHEMY_ENGINE_STRING = 'sqlite:////{}'.format(DATABASE_PATH)

# Clean Data config
Columns = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research']
Target = 'Chance of Admit '
fig_direcotry = './figures'
Transform_col = 'CGPA'
Path_To_Clean_File = './data/clean.csv'

# Model Selection config
split_params = {"test_size": 0.25,
                "random_state": 1995
                }
model_params_r2 = {"scoring": 'r2',
                   'random_state': 1995,
                   "test_size": 0.3,
                   "cv": 3
                   }
model_params_rmse = {"scoring": 'neg_mean_squared_error',
                     'random_state': 1995,
                     "test_size": 0.3,
                     "cv": 3
                     }
Selection_Perform_Path = './models/model selection.csv'

# Train model config
Random_state = 1995
Feature_Plot_Name = 'feature_importance.png'
Final_Mode_Eval_Path = './models/final model metric.csv'
Model_CSV_Path = './models/final model.csv'
Model_Pickle_Path = './models/final model.pkl'
