#!/bin/bash

# Fill with proper data

echo "begin ...."

SONAR_URL = ''
SONAR_USER = ''
SONAR_PASSWORD = ''
INFLUX_URL = ''
INFLUX_TOKEN = ''
INFLUX_ORG = ''
INFLUX_BUCKET = ''
INTERVAL = 86400

python sonar-client.py

echo "End!"
