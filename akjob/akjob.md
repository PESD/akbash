# Akjob
## Daemon
The daemon starts when Akbash starts. That code is in akjob.apps. There is no
monitoring to restart the daemon if it crashes or otherwise stop. A cronjob
could be created to attempt to start the daemon periodically. The daemon will
not start if it it's already running.
## Scheduling Job
To schedule a job, create an instance of akjob.models.Job. Set the attributes
and save. You must set the name attribute with a job name. The name does not
need to be unique.
### akjob.models.Job
#### Attributes
* name - Required field. string

**One off job attributes:**
* **run_once_at** - datetime. The job will run at the time specified in the datetime object.

**Reoccuring job attributes:**
* **run_every** - timedelta. The job runs after the time interval specified in the timedelta object or pendulum interval object. 
