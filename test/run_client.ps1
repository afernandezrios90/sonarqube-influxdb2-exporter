# Fill with proper data
$env:SONAR_URL = ''
$env:SONAR_USER = ''
$env:SONAR_PASSWORD = ''
$env:INFLUX_URL = ''
$env:INFLUX_TOKEN = ''
$env:INFLUX_ORG = ''
$env:INFLUX_BUCKET = ''
$env:INTERVAL = 86400

& 'python.exe' '{path_to_file}\sonar-client.py' 