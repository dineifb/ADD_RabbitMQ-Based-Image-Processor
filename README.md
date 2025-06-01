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