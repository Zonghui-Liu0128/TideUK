FROM python:3.8

WORKDIR /home/tides

COPY requirements.txt

COPY app.py

COPY process.py

COPY process_stations.py

COPY stations.csv

COPY tideReadings.csv

ADD requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "process.py" ]
