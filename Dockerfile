FROM python:3.6-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY sonar-client.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "./sonar_collector_docker/sonar-client.py" ]