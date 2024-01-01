FROM python:3.11-slim
RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY crontab /etc/cron.d/
COPY requirements.txt .
COPY direntree.py .
COPY tclient.py .
COPY clogger.py .
COPY msync.py .

ARG TR_HOST_PORT
ARG TR_HOST_IP
ARG TR_PATH
ARG TR_USER
ARG TR_PASS
ARG JF_MOVIES
ARG JF_SHOWS
ARG JF_PATH
ARG LOG_LEVEL

RUN echo "TR_HOST_PORT=$TR_HOST_PORT" >> /etc/environment
RUN echo "TR_HOST_IP=$TR_HOST_IP" >> /etc/environment
RUN echo "TR_PATH=$TR_PATH" >> /etc/environment
RUN echo "TR_USER=$TR_USER" >> /etc/environment
RUN echo "TR_PASS=$TR_PASS" >> /etc/environment
RUN echo "JF_MOVIES=$JF_MOVIES" >> /etc/environment
RUN echo "JF_SHOWS=$JF_SHOWS" >> /etc/environment
RUN echo "JF_PATH=$JF_PATH" >> /etc/environment
RUN echo "LOG_LEVEL=$LOG_LEVEL" >> /etc/environment

RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log
RUN pip3 install -r requirements.txt
RUN crontab /etc/cron.d/crontab

CMD cron && tail -f /var/log/cron.log
