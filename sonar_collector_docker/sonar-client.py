import requests
import os
import datetime
import time 

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

BASE_URL = os.getenv('SONAR_URL', 'http://sonar.yourGroup.com:9876')
USER = os.getenv('SONAR_USER', 'admin')
PASSWORD = os.getenv('SONAR_PASSWORD', 'admin')
INFLUX_URL = os.getenv('INFLUX_URL', '192.168.0.1')
INFLUX_TOKEN = os.getenv('INFLUX_TOKEN', '')
INFLUX_ORG = os.getenv('INFLUX_ORG', '')
INFLUX_BUCKET = os.getenv('INFLUX_BUCKET', '')
INTERVAL = os.getenv('INTERVAL', 86400)

class SonarApiClient:

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def _make_request(self, endpoint):
        r = requests.get(BASE_URL + endpoint, auth=(self.user, self.passwd))
        return r.json()
    
    def get_all_projects(self, endpoint):
        data = self._make_request(endpoint)
        projects = []
        for component in data['components']:
            dict = {
                'id': component['id'],
                'key': component['key'],
                'name': component['name'],
                'tags': component['tags']
            }
            projects.append(dict)
        return projects
    
    def get_all_available_metrics(self, endpoint):
        data = self._make_request(endpoint)
        metrics = []
        for metric in data['metrics']:
            if metric['type'] in ['INT','MILLISEC','WORK_DUR','FLOAT','PERCENT','RATING']:
                metrics.append(metric['key'])
	    
        metric_set = set(metrics)		
        return metric_set
    
    def get_measures_by_component_id(self, endpoint):
        data = self._make_request(endpoint)
        return data['component']['measures']

class InfluxApiClient:

    def __init__(self):
        pass

    def connect(self):
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
        influx_write_api = client.write_api(write_options=SYNCHRONOUS)
        return influx_write_api

class Project:

    def __init__(self, identifier, key, name, tags):
        self.id = identifier
        self.key = key
        self.name = name
        self.tags = tags
        self.metrics = None
        self.timestamp = datetime.datetime.utcnow().isoformat()

    def set_metrics(self, metrics):
        self.metrics = metrics
    
    def generate_points(self):
        points = []
        '''
        'metrics' is an array of metrics with the following formats:
        METRIC + VALUE --> {'metric': 'comment_lines', 'value': '15'},
        METRIC + VALUE + BESTVALUE --> {'metric': 'blocker_violations', 'value': '0', 'bestValue': True},
        METRIC + PERIODS[INDEX + VALUE + BESTVALUE --> {'metric': 'new_duplicated_lines', 'periods': [{'index': 1, 'value': '0', 'bestValue': True}]}
        '''
        for metric in self.metrics:
            # Control of metrics content to access the value appropriately
            if 'periods' in metric:
                period_array = metric['periods']
                value = period_array[0].get('value', 0)
            else:
                value = metric.get('value', '0')
            # Generation of each metric point in influx format
            point = {
                'measurement': metric['metric'],
                'tags': {
                    'id': self.id,
                    'key': self.key,
                    'name': self.name,
                    'tags': "|".join(self.tags)
                },
                'fields': {
                    'value': float(value)
                },
                'time': self.timestamp
            }
            points.append(point)
        return points

### MAIN ###

# Read selected metrics for file 'metrics.txt'
# For testing on Windows
#with open(os.path.dirname(os.path.realpath(__file__))+'\metrics.txt') as file:
with open(os.path.dirname(os.path.realpath(__file__))+'/metrics.txt') as file:
    selected_metrics = file.read().splitlines()
selected_metrics_set = set(selected_metrics)

count=0

while True:
    count += 1
    print ("count -----")
    print (count)

    print ("begin export data...")
    # Fetch all projects IDs
    sonar_client = SonarApiClient(USER, PASSWORD)
    projects = sonar_client.get_all_projects('/api/components/search_projects?ps=250')
    
    # Fetch all available metrics (as a set)
    metric_set = sonar_client.get_all_available_metrics('/api/metrics/search?ps=150')
    
    # Check if all selected metrics are available in SonarQube metric list
    if selected_metrics_set.issubset(metric_set):
        comma_separated_metrics = ','.join(selected_metrics)
    else:
        print("Error: one or more metrics in the configuration file does not exist in SonarQube")
        exit(1)
    # Declare influxdb connection
    influx_client = InfluxApiClient()
    influx_write_api = influx_client.connect()

    # Declare the set of tags
    tags = set()

    # Collect metrics per project
    uri = '/api/measures/component'
    for item in projects:
        project_id = item['id']
        project_key = item['key']
        project_name = item['name']
        project_tags = item['tags']
        # If project tags is empty, update the set
        if len(project_tags):
            tags.update(project_tags)

        project = Project(project_id, project_key, project_name, project_tags)
        component_id_query_param = 'componentId=' + project_id
        metric_key_query_param = 'metricKeys=' + comma_separated_metrics
        measures = sonar_client.get_measures_by_component_id(uri + '?' + component_id_query_param + '&' + metric_key_query_param)
        project.set_metrics(measures)

        # Expose the metrics
        points = project.generate_points()
        influx_write_api.write(INFLUX_BUCKET, INFLUX_ORG, points)

        # Expose the tags
        tag_points = []
        for tag in tags:
            tag_point = {
                'measurement': 'tag',
                'tags': {
                    'tag': tag
                },
                'fields': {
                    'value': 1.0
                },
                'time': datetime.datetime.utcnow().isoformat()
            }
            tag_points.append(tag_point)
        influx_write_api.write(INFLUX_BUCKET, INFLUX_ORG, tag_points)

    print('Waiting for next execution...')
    time.sleep(int(INTERVAL))
