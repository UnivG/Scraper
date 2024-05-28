FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scraper.py .

RUN apt-get update && apt-get -y install cron && \
    echo "0 */3 * * * /usr/local/bin/python /app/scraper.py >> /var/log/cron.log 2>&1" > /etc/cron.d/scraping-cron && \
    chmod 0644 /etc/cron.d/scraping-cron && \
    crontab /etc/cron.d/scraping-cron && \
    touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
