FROM python:3.9-slim

RUN apt-get update && apt-get -y install cron && \
    pip install pymongo

COPY backup.py /app/backup.py

RUN mkdir -p /app/backup

RUN /usr/local/bin/python /app/backup.py

RUN echo "0 2 * * * /usr/local/bin/python /app/backup.py >> /var/log/cron.log 2>&1" > /etc/cron.d/backup-cron && \
    chmod 0644 /etc/cron.d/backup-cron && \
    crontab /etc/cron.d/backup-cron && \
    touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
