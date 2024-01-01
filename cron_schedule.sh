#!/bin/sh

COMMAND="/usr/local/bin/python /app/msync.py --loglevel $LOG_LEVEL --$VERBOSE >> /var/log/cron.log 2>&1"
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $COMMAND") | crontab -

