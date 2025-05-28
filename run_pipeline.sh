#!/bin/bash

# Start uploader.py in new Terminal tab
osascript -e 'tell application "Terminal" to do script "cd \"$(pwd)\"; python3 uploader.py"'

sleep 1

# Start processor.py in another Terminal tab
osascript -e 'tell application "Terminal" to do script "cd \"$(pwd)\"; python3 processor.py"'

sleep 1

# Run producer.py in the current Terminal
python3 producer.py




### ONlY PUT ON TERMINAL   "./run_pipeline.sh"     AND EVERYTHING WILL RUN IN THE RIGHT ORDER: ./run_pipeline.sh