#!/bin/bash

URL=http://localhost:8000/api/rest/v1/heartbeat/
LOG=/home/daneos/src/projekt/heartbeat.log

curl -s $URL >> $LOG
echo >> $LOG