# SonarQube - InfluxDB2 2.0 exporter
---

**Stack**:  sonarqube、influxdb、grafana、docker

This exporter is a fork of the original [sonarqube exporter](https://github.com/qinrui777/sonarqube-metric-to-grafana), updated to be compatible to InfluxDB 2.0.
Also, control file has been added to be able to pre-select the desired metrics from SonarQube, instead of reading the complete metric list.

####  Data flow diagram

![picture](https://github.com/afernandezrios90/sonarqube-influxdb2-exporter/blob/master/images/Dataflow.png)

### Main features

The exporter allows to gather the following metrics:
- All available metrics in SonarQube
- All active projects and their metrics and tags
- The list of tags used to use tag filter in the dashboards

Constraints:
- Proper tagging system is highly encouraged in SonarQube. Project with no tag won't be displayed as the pre-filter is done by tags.

### Grafana dashboards

Two sample dashboard definitions are provided as well:
- Detailed dashboard
  - User is able to select one project, pre-filtering by tag
  - For a given project, it displays the last value of 4 most common rates: Reliability rating, Security rating, Technical Debt rating & Cove coverage   
  - For a given project, it displays the historical value of 4 most common metrics: bugs, vulnerabilities, code coverage & code smells

- Executive dashboard
  - User is able to select one tag
  - For a given tag, it displays the historical value of 4 most common metrics for all the projects with that tag: bugs, vulnerabilities, code coverage & code smells


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
