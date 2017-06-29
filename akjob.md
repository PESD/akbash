# Daemon
The daemon starts when Akbash starts. There is no monitoring to restart the daemon if it crashes or otherwise stop. A cronjob could be created to attempt to start the daemon periodically.
# akjob.models.Job
Pendulum: https://pendulum.eustace.io/
Shortcuts to Pendulum:
* Job.interval
* Job.datetime
* Job.now