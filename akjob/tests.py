"""
Things to test:
* daemon control and daemon start / stop
    * start command starts daemon
    * stop command stops daemon
    * if daemon is running don't start another one
"""

import os
from akjob import akjobd
from django.test import TestCase
