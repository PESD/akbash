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
This job will run every 2 hours and execute ```print("Hello", "World")```. The print statement will not actually accomplish anything as that process is not connected to a console.
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

TODO: Documentation on using akjob's logging in custom job code objects.

## Creating and Scheduling Jobs
### Overview
Jobs are created and scheduled by saving an instance of akjob.models.Job. Create an instance of akjob.models.Job. Set the various scheduling attributes. Set the job_code_object attribute using an object containing the code to run. Save the instance.
### Job Code Objects
To execute job code, akjob will call the run(self) method contained in the object stored in job_code_object. You may create your own containers with run() methods that contain your code to be executed.

Alternatively, the class **akjob.models.JobCallable** is provided.
```akjob.models.JobCallable(callable, *args, **kwargs)```
When creating an instance of JobCallable, provide a callable object and any arguments the callable requires. The JobCallable instance contains a run() method that will call the callable using the provided arguments.

The job code object will be pickeled and stored in the database. Make sure everything within may be pickeled. http://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled
### Scheduling and Limiting Job Execution
Types of scheduling:
* You may specify specific dates and times when the job executes. A list of datetimes is used.
* You may specify an interval when the job executes. For instance, execute every 15 minutes. A datetime.timedelta is used.
* You may schedule execution times on a monthly or weekly basis. In other words, you may provide a list of days of the month and the job will execute on those day. For weekly jobs, you provide a list of days of the week. Along with a list of days, you must also specify a time of the day the job should execute.

In addition to scheduling when a job should execute, you may specify when the job should not execute. For example, a job could be scheduled using an interval of 1 hour but have limit set to only allow the job to run between the hours of 6 AM and 6 PM. The job will execute every hour between 6 AM and 6 PM each day.

Types of limits and restrictions:
* You may stop a job from executing using a generic enabled and disabled flag.
* You may limit the number of times a job is executed. If a job reaches the run count limit, it will no longer execute.
* You may limit job execution to a window of time each day. For example, only run the job between 9 AM and 5 PM.
* You may limit job execution to
    * specific days of the week
    * specific days of the month
    * specific months
    * specific dates
### The Scheduling Atrributes of akjob.models.Job
##### Specific Date and Time Job Attributes
**`dates`** - A [related manager](https://docs.djangoproject.com/en/1.11/ref/models/relations/) for `akjob.models.JobDates`. The `JobDates.job_datetime` field holds a `datetime.datetime` representing a date and time the job should run.

**`dates_list`** - `list` containing `datetime.datetime` objects. This is a property and is an alternate interface to `dates`. The job will run at the dates and times specified in the datetime objects. Be aware that list methods may not fire the property's setter.

```python
from akjob.models import Job, JobCallable
from datetime import datetime, timezone
myjob_code = JobCallable(somefunc, "arg1", "arg2", arg3="arg3stuff")
runtime1 = datetime(2017, 11, 25, 14, 30, tzinfo=timezone.utc)
runtime2 = datetime(2017, 12, 18, 18, 10, tzinfo=timezone.utc)

myjob1 = Job.objects.create(name="Job Test 1")
myjob1.dates.create(job_datetime=runtime1)
myjob1.dates.create(job_datetime=runtime2)
myjob1.job_code_object = myjob_code
myjob1.save()

# Do the same thing using the dates_list property.
myjob2 = Job.objects.create(name="Job Test 2")
myjob2.dates_list = [runtime1, runtime2]
myjob2.job_code_object = myjob_code
myjob2.save()
```
##### Reoccuring Job Attributes
**== Intervals ==**
**`run_every`** - `datetime.timedelta`. The job runs after the time interval specified in the timedelta object. 

**== Monthly ==**
**`monthly_days`** - A `ManyToManyField` linking to `akjob.models.DayOfMonth`. Set monthly_days using `integer` or `DayOfMonth` objects to represent the days of the month you want the job to run. For example, setting 1 and 15 means the job will run on the 1st and 15th of the month.

**`monthly_days_list`** - `list` containing `integer` or `DayOfMonth` objects. This is a property and is an alternate interface to `monthly_days`. Be aware that list methods may not fire the property's setter.

**`monthly_time`** - `datetime.time`. The time of day when the monthly job should run.

**`monthly_time_tz_offset_timedelta`** - `datetime.timedelta`. Set this to the needed timezone offset using a datetime.timedelta. This field defaults to UTC / timedelta(0) so there is no need to set it if UTC is the timezone. This field is required because of problems between django and MS SQL Server.

**== Weekly ==**
**`weekly_days`** - A `ManyToManyField` linking to `akjob.models.DayOfWeek`. Set weekly_days using `integer` or `DayOfWeek` objects to represent the days of the week you want the job to run. Use integers or `DayOfWeek` objects starting at 1 for Sunday, 2 for Monday, and so on to 7 for Saturday.

**`weekly_days_list`** - `list` containing `integer` or `DayOfWeek` objects. This is a property and is an alternate interface to `weekly_days`. Be aware that list methods may not fire the property's setter.

**`weekly_time`** - `datetime.time`. The time of day when the weekly job should run.

**`weekly_time_tz_offset_timedelta`** - `datetime.timedelta`. Set this to the needed timezone offset using a datetime.timedelta. This field defaults to UTC / timedelta(0) so there is no need to set it if UTC is the timezone. This field is required because of problems between django and MS SQL Server.
```python
from akjob.models import Job, JobCallable
from datetime import time, timedelta
myjob_code = JobCallable(somefunc, "arg1", "arg2", arg3="arg3stuff")

# A job that runs every 15 minutes
myjob1 = Job.objects.create(name="Interval")
myjob1.run_every = timedelta(minutes=15)
myjob1.job_code_object = myjob_code
myjob1.save()

# A job that runs on the 1st and 15th day of each month at 1:30 AM UTC.
myjob2 = Job.objects.create(name="Monthly")
myjob2.monthly_days_list = [1, 15]
myjob2.monthly_time = time(1, 30)
myjob2.job_code_object = myjob_code
myjob2.save()

# A job that runs each weekday at 10 PM MST (UTC -7 not considering DST)
myjob3 = Job.objects.create(name="Weekdays 10PM somefunc")
myjob3.weekly_days_list = [2, 3, 4, 5, 6]
myjob3.weekly_time = time(22, 0)
myjob3.weekly_time_tz_offset_timedelta = timedelta(hours=-7)
myjob3.job_code_object = myjob_code
myjob3.save()
```
### The Schedule Limiting Atrributes of akjob.models.Job
##### Job Enabled Flag and Restricting the Number of Runs
**``job_enabled``** - ``boolean``. If set to False, the job will not be executed. Defaults to True so you don't need to set this unless you want to disable the job.

**``run_count_limit``** - ``integer``. This will limit the number of times the job is executed. If the _run_count attribute is equal or greater than run_count_limit the the job is not executed. The print method of the job will display the run count.

##### Limit Runs to a Window of Time Each Day
Job runs will be limited to only run, each day, within the window of time defined by active_time_begin and active_time_end. The timezone offset must be defined using a timedelta in active_time_tz_offset_timedelta.
* **``active_time_begin``** - ``datetime.time``.
* **``active_time_end``** - ``datetime.time``.
* **``active_time_tz_offset_timedelta``** - ``datetime.timedelta``. Defaults to timedelta(0) which is UTC.

##### Limit Job Runs to Specific Days of the Month
**``active_monthly_days``** - A `ManyToManyField` linking to `akjob.models.DayOfMonth`. Limit job runs to the given days of month. Use ``integer`` or ``DayOfMonth`` objects for each day you want to limit activity to. Ex., 1,15 means limit the run to the 1st and 15th of each month.

**``active_monthly_days_list``** - ``list`` containing ``integer`` or ``DayOfMonth`` objects. This is a property and is an alternate interface to active_monthly_days. Be aware that list methods may not fire the property's setter.

##### Limit Job Runs to Specific Days of the Week
**``active_weekly_days``** - A `ManyToManyField` linking to `akjob.models.DayOfWeek`. Limit job runs to the given days of week. Use ``integer`` or ``DayOfWeek`` objects for each day starting at 1 for Sunday, 2 for Monday, and so on to 7 for Saturday.

**``active_weekly_days_list``** - ``list`` containing ``integer`` or ``DayOfWeek`` objects. This is a property and is an alternate interface to active_weekly_days. Be aware that list methods may not fire the property's setter.

##### Limit Job Runs to Specific Months
**`active_months`** - A `ManyToManyField` linking to `akjob.models.Months`. Limit job runs to the given months. Use `integer` or `Months` objects for each month using 1 for January, 2 for February up to 12 December.

**`active_months`** - `list` containing `integer` or `Months` objects. This is a property and is an alternate interface to active_months. Be aware that list methods may not fire the property's setter.

##### Limit Job Runs to a Specific Date Range.
Provide beggining and end dates using datetime.time objects to define a date range in which the job may run. Job run times out side of the date range will not execute.
**`active_date_begin`** - `datetime.date`.
**`active_date_end`** - `datetime.date`.

#### Example
```python
from akjob.models import Job, JobCallable
from datetime import time, timedelta
myjob_code = JobCallable(somefunc, "arg1", "arg2", arg3="arg3stuff")

# A job that runs every 15 minutes on weekdays
#   between 8 AM and 4 PM MST (UTC -7 not considering DST.)
myjob1 = Job.objects.create(name="Interval")
myjob1.run_every = timedelta(minutes=15)
myjob1.active_time_begin = time(8)
myjob1.active_time_end = time(16)
myjob1.active_time_tz_offset_timedelta = timedelta(hours=-7)
myjob1.active_weekly_days_list = [2, 3, 4, 5, 6]
myjob1.job_code_object = myjob_code
myjob1.save()
```

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

#### showinfo
Display information about the job specified by the -id argument.

## Known Issues, Quirks, and Work Arounds
When a new job is created, akjob will not actually schedule the job to be
executed until the job is ran in akjobd's loop. So it's possible your 1st
expected job execution run won't happen if it's close to the job creation time
and hasn't yet been through akjobd's loop. To avoid this problem, run the job's
next_run() method. This will schedule the 1st run right away. I just thought of
something that needs to be tested. Will a similar problem occur if you've used
run limits? Might the 1st run after a limit passes be skipped?

When a new run_every (interval) job is created with limits specified, if created at a time outside run limits, there is some behavior that may seem unexpected to the user. The jobs works correctly but it may appear as inactive in management command `akjobd joblist` and self._next_run may be None. It will work correctly but this behavior could be confusing to the user. Running the job's next_run() method after job creation migth avoid this problem but not always.

The _job_running attribute is set to True before the job code is executed and is set back to false after the execution. Akjobd will not execute the job if _job_running is True. If for some reason things crash before _job_running is set back to False, the job will no longer be executed. The log file will show "Job didn't run because job running flag is True."
