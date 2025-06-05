# How it works

## Run in separate terminals:

python uploader.py

python processor.py

python producer.py


### Inspect DB:

python  inspect_db.py


## if some of the images are not added to the DB:

python resend_missing.py

## if in the output of inspect_db some predictions are None:

resend_unprocessed.py


## to delete the DB: 

rm image_predictions.db


## to initialize the DB:

python init_db.py


## to purge current queues 

sudo rabbitmqctl purge_queue raw_data

sudo rabbitmqctl purge_queue processed_data

## Run the presenter API (query predictions via web):

pip install -r requirements.txt
uvicorn presenter_api:app --reload

# Endpoints:
#   /predictions                -> Returns all predictions as JSON
#   /predictions/{image_name}   -> Returns the prediction of a given image as JSON

# Web UI:
#   http://127.0.0.1:8000/      http://127.0.0.1:8000/predictions/html 
You can see the forecasts in tabular form