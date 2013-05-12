import os
import logging

EXIT=False

# STATUSES 
STOPPED=0
STARTED=1
PAUSED=2

# WORK_STATUS
WORKING =""
RESTING ="rest-"

# WORK_TIME
WORK_TIME = 25
REST_TIME = 5
STOP_TIME = 5
WORK_CICLES = 1

# Constants
SECONDS=1
MINUTES=60*SECONDS
HOURS=60*MINUTES
DAYS=24*HOURS

NOTIFY_TIME = 5*MINUTES

ROOT=os.path.dirname(__file__) 
MEDIA=ROOT+"/../data/media/" 

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
LOG_LEVEL = logging.DEBUG
