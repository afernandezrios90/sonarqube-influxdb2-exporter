FROM python:3.6-alpine

WORKDIR /usr/src/app
COPY sonar_collector_docker/requirements.txt ./
COPY sonar_collector_docker/sonar-client.py ./
COPY sonar_collector_docker/metrics.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "./sonar-client.py" ]