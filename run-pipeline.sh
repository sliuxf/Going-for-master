# Acquire raw data from S3 bucket
python3 ./src/acquire.py

# clean data set, Generate features
python3 ./src/clean.py

# Try different models
python3 ./src/model_selection.py

# Train model
python3 ./src/train_model.py
