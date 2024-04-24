FROM python:3.11

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY crontab /etc/crontab
COPY requirements.txt ./
COPY main.py /app/main.py

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/crontab

RUN /usr/bin/crontab /etc/crontab

# run crond as main process of container
CMD printenv >> /etc/environment && cron -f