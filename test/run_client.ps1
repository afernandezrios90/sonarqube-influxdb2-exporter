$env:SONAR_URL = 'http://wfsonarprod.sidmar.be:9000'
$env:SONAR_USER = 'SYS-MONAUT'
$env:SONAR_PASSWORD = 'MonAutForScaleUp'
$env:INFLUX_URL = 'http://localhost:8086/'
$env:INFLUX_TOKEN = '1XwX3LuWp1gCNBqz5BHit6fswCJEtNMub32FXAILIjo5kYa80h42rYlcH9QmZhmumdwujuKyVNiW9epdp2ymPQ=='
$env:INFLUX_ORG = 'AM'
$env:INFLUX_BUCKET = 'sonarqube'
$env:INTERVAL = 86400

& 'C:\Users\A0790581\AppData\Local\Programs\Python\Python310\python.exe' 'C:\DEV\git\sonarqube-influxdb2-exporter\sonar_collector_docker\sonar-client.py' 