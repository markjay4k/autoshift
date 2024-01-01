#!/bin/bash

# script to start crontab command

COMMAND="/usr/local/bin/python /app/msync.py --loglevel $LOG_LEVEL --verbose >> /var/log/cron.log 2>&1"
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $COMMAND") | crontab -

