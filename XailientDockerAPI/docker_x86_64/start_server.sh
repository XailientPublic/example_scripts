#!/bin/bash

#Copyright 2021 Xailient Inc.
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#documentation files (the "Software"), to deal in the Software without restriction, including without 
#limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
#of the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or 
#substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
#AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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