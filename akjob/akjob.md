# Akjob
## The Akjobd Daemon
The akjobd daemon loops through all jobs stored in the database and runs them. If the job is not schedule to run at that time, the job will perform no actions. After akjobd runs all the jobs, it sleeps for 1 minute then starts the loop again.

The daemon starts when Akbash starts. That code is in akjob.apps. You may set the environment variable AKJOB_START_DAEMON to "False" to tell django not to start the daemon. This is useful for development instances.

There is no monitoring to restart the daemon if it crashes or otherwise stops. A cronjob could be created to attempt to start the daemon periodically. This is safe because the daemon will not start if it's already running.

Akjobd uses a pid file to determine wether the daemon is already running or not. The default pid file is BASE_DIR/akjob/akjobd.pid. Environment variables or changing the akjobd launch options can be used to change the pid file though I don't know why you would want to do that.

When akjobd is launched via django startup, via akjob.apps, it is ran in a separate process so that the parent django process may continue on as normal.

There is an akjobd management command available. Using the start, stop, and restart options allows you to start, stop, and restart the akjobd daemon.

This is not normal but there is a small possibility that when you make a change to a job, the akjobd daemon might be reading from a cache and not see that change. You may need to restart the daemon so the change is picked up. Again, this is not typical.
## Scheduling Jobs
To schedule a job, create an instance of akjob.models.Job. Set the attributes and save. You must set the name attribute with a job name. The name does not need to be unique.
### akjob.models.Job
#### Attributes
* name - Required field. string

**One off job attributes:**
* **run_once_at** - datetime. The job will run at the time specified in the datetime object.

**Reoccuring job attributes:**
* **run_every** - timedelta. The job runs after the time interval specified in the timedelta object or pendulum interval object. 

## Management Commands
The first argument, after "akjobd", is the action the command should perform.
Example: ```python manage.py akjobd stop```
#### stop, start, restart
Stop, start, or restart the akjobd daemon. The options -pd / --piddir, and -pn / --pidname may be used to specify the pid file to use.
#### reloadfixture
Clears out the DayOfMonth, DayofWeek, and Months tables then reloads them. This is useful if you accidently insert extra data into these tables or accidently delete needed records.
#### joblist
Display a list of all jobs.
#### enablejob, disablejob
Set the job_enabled attribute in a Job instance object. To either enable or disable the job. Using "enablejob" sets the attribute to True and "disablejob" sets the attribute to False. You must use the -id argument to specify the id number of the job.
#### deletejob
Delete the job specified by the -id argument.

