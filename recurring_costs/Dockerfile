FROM python:3.11

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/crontab
COPY main.py /app/main.py

RUN chmod 0644 /etc/crontab

RUN /usr/bin/crontab /etc/crontab

# run crond as main process of container
CMD printenv >> /etc/environment && cron -f