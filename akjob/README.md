# Akjob
The job scheduling app used by Akbash. Akbash already uses the term "Task" so here we've stuck to using the term "Job" to avoid confusion.
### Example
```python
from akjob.models import Job, JobCallable
from datetime import timedelta
myjob_code = JobCallable(print, "Hello", "World")
myjob = Job()
myjob.job_code_object = myjob_code
myjob.name = "Print Hello World"
myjob.run_every = timedelta(hours=2)
myjob.save()
```
This job will run every 2 hours and execute ```print("Hello", "World")```. The print statement will not actually acomplish anything as that process is not connected to a console.
## The Akjobd Daemon
The akjobd daemon loops through all jobs stored in the database and runs them. If the job is not schedule to run at that time, the job will perform no actions. After akjobd runs all the jobs, it sleeps for 1 minute then starts the loop again.

The daemon starts when Akbash starts. That code is in akjob.apps. You may set the environment variable AKJOB_START_DAEMON to "False" to tell django not to start the daemon. This is useful for development instances.

There is no monitoring to restart the daemon if it crashes or otherwise stops. A cronjob could be created to attempt to start the daemon periodically. This is safe because the daemon will not start if it's already running.

Akjobd uses a pid file to determine wether the daemon is already running or not. The default pid file is BASE_DIR/akjob/akjobd.pid. Environment variables or changing the akjobd launch options can be used to change the pid file though I don't know why you would want to do that.

When akjobd is launched via django startup, via akjob.apps, it is ran in a separate process so that the parent django process may continue on as normal.

There is an akjobd management command available. Using the start, stop, and restart options allows you to start, stop, and restart the akjobd daemon.

This is not normal but there is a small possibility that when you make a change to a job, the akjobd daemon might be reading from a cache and not see that change. You may need to restart the daemon so the change is picked up. Again, this is not typical.
### Logging
You may want to examine the log files written by akjob to confirm your job is running without problems. The log files are located in BASE_DIR/akjob/logs. The log files rotate once a day and only 15 days of logs are kept.

Akjob logging is a mess. Multiple files are used because when akjobd daemonized, all file descriptors are closed so new ones need to be opened. Also, the logging documentation says you should not log to the same file from different processes (from different modules is fine if they're ran in the same process). The akjobd daemon runs from a different process then django so multiple files need to be used. The python logging module seem to choose to use whatever the last logging file handler that was used so logging seems to jump around between files. 

Here are some ideas to improve logging in future versions. Use a more standard python logging setup that uses propogation. Configure the daemon to not close the logging file descriptors when it deamonizes.
## Creating and Scheduling Jobs
### Overview
Jobs are created and scheduled by saving an instance of akjob.models.Job. Create an instance of akjob.models.Job. Set the various scheduling attributes. Set the job_code_object attribute using an object containing the code to run. Save the instance.
### Job Code Objects
To execute job code, akjob will call the run() method contained in the object stored in job_code_object. You may create your own containers with run() methods that contain your code to be executed.

Alternatively, the class **akjob.models.JobCallable** is provided.
```akjob.models.JobCallable(callable, *args, **kwargs)```
When creating an instance of JobCallable, provide a callable object and any arguments the callable requires. The JobCallable instance contains a run() method that will call the callable using the provided arguments.

The job code object will be pickeled and stored in the database. Make sure everything within may be pickeled. http://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled
### Scheduling and Limiting Job Execution
Types of scheduling:
* You may specify specific dates and times when the job executes. A list of datetimes is used.
* You may specify an interval when the job executes. For instance, execute every 15 minutes. A datetime.timedelta is used.
* You may schedule execution times on a monthly or weekly basis. In other words, you may provide a list of days of the month and the job will execute on those day. For weekly jobs, you provide a list of days of the week. Along with a list of days, you must also specify a time of the day the job should execute.

In addition to scheduling when a job should execute, you may specify when the job should not execute. An example of how this is useful: A job could be schedule using an interval of 1 hour but only run between the hours of 6 am and 6 pm.

Types of limits and restrictions:
* You may stop a job from executing using a generic enabled and disabled flag.
* You may limit the number of times a job is executed. If a job reaches the run count limit, it will no longer execute.
* You may limit job execution to a window of time each day. For example, only run the job between 9 am and 5 pm.
* You may limit job execution to
    * specific days of the week
    * specific days of the month
    * specific months
    * specific dates
### The Atrributes of akjob.models.Job
* name - Required field. string

**One off job attributes:**
* **run_once_at** - datetime. The job will run at the time specified in the datetime object.

**Reoccuring job attributes:**
* **run_every** - timedelta. The job runs after the time interval specified in the timedelta object or pendulum interval object. 
## Job Code
job_code_object
JobCallable
#### logging
Which log file to log to.
## The akjobd Management Command
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

