#!/bin/bash

###############
#  RUN BASIC SCRIPT  #
###############

echo 'RUNNING XAILIENT DETECTOR SDK API'

LOCATION=$(python3.7 -m pip show xailient | 
egrep '^Location: .+' | 
sed 's/Location: //')

cd "$LOCATION"
cd xailient/
cd scripts

echo $LOCATION

# Register the deivce and wait for a couple of seconds
echo "Uninstalling previous installations..."
python3 -m xailient.uninstall
sleep 2

echo "Registering device..."
python3 -m xailient.install


cp /app/detection_api.py ../samples/.

cd ../samples/.

python3 -u detection_api.py

if [ $? -eq 0 ]; then
	echo "\SERVER STARTED ..."
else
	echo "\nError: Inference failed"#
	echo 'Contact support@xailient.com'
fi