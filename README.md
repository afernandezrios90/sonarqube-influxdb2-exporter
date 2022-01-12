# SonarQube - InfluxDB2 2.0 exporter
---

**Stack**:  sonarqube、influxdb、grafana、docker

This exporter is a fork of the original [sonarqube exporter](https://github.com/qinrui777/sonarqube-metric-to-grafana), updated to be compatible to InfluxDB 2.0.
Also, control file has been added to be able to pre-select the desired metrics from SonarQube, instead of reading the complete metric list.

####  Data flow diagram

![picture](https://github.com/afernandezrios90/sonarqube-influxdb2-exporter/blob/master/images/Dataflow.png)

### Build the exporter from the repo
```bash
docker build https://github.com/afernandezrios90/sonarqube-prometheus-exporter.git -t {yourDockerRepo}/sonarqube-influxdb2-exporter
```

### Deployment using Docker
```bash
docker run -d --name sonarqube-influxdb2-exporter \
-e SONAR_URL={url} \
-e SONAR_USER={user} \
-e SONAR_PASSWORD={pw} \
-e INFLUX_URL={url} \
-e INFLUX_TOKEN={token} \
-e INFLUX_ORG={organization} \
-e INFLUX_BUCKET={bucket} \
-e INTERVAL=86400 \ 
{yourDockerRepo}/sonarqube-influxdb2-exporter
```

Subtitute the values with the appopriate ones of your environment
