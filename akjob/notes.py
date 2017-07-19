"""
Schedule and run jobs. Run as a daemon.

Consider using python-daemon (https://pagure.io/python-daemon) to create a
    deamon process.
Consider using signal to catch things such a shutdown signals. python-daemon
uses signal.

Another route is to use RabbitMQ + Celery + django-celery.

Create job class. job objects submitted to scheduler.

scheduler Methods:
List jobs, delete jobs, add jobs.

one time jobs, recuring jobs, recuring jobs that can delete themselves when
mission accomplished.

Submit job. Pass an object containing the job code along with scheduling
options. Or submit funtion/method to be ran with needed paramaters/args.

python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

Do I need to define what to do in response to diferent signals or is the
default that python-daemon uses good enough?

This module should be moved under it's own package?
I think I could start the scheduler daemon from akbash.__init__? I guess that's
not correct and your supposed to use AppConfig.ready()?

TODO:
* Create job class
* Create model
"""
