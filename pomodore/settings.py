# The MIT License (MIT)

# Copyright (c) <year> <copyright holders>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

# Time that shows message popup
NOTIFY_TIME = 5*MINUTES

ROOT=os.path.dirname(__file__) 
MEDIA=ROOT+"/../data/media/" 

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
LOG_LEVEL = logging.DEBUG
