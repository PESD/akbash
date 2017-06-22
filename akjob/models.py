from django.db import models

class Job(models.Model):
    "Job definitions"

    MONTHS = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December")
    )

    DAYS = (
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
    )

    """ Schedule One off job """
    run_once_at = models.DateTimeField(
        blank=True,
        help_text="Date and time to run the job. Used for one off job runs.")

    """ Schedule reoccuring jobs """
    run_every = models.DurationField(
        blank=True,
        help_text="Run every ___. Format: [DD] [HH:[MM:]]ss. Schedule the job" +
                  "to repeatedly run after a time interval. Ex., Run every" +
                  "05:00 (5 minutes)")
    run_monthly = models.CharField(
        blank=True,
        help_text="Comma seperated list of days of the month to run the job." +
                  " Ex., 1,15 means run on the 1st and 15th of each month.")
    run_weekly = models.CharField(blank=True)  # Day of week
    run_monthly_time = models.TimeField(blank=True)
    run_weekly_time = models.TimeField(blank=True)
    # Run this many times. Count down each run.
    run_count_limit = models.IntegerField(blank=True)

    """ Limit job run to a window of time. """
    active_time_begin = models.TimeField(blank=True)
    active_time_end = models.TimeField(blank=True)
    active_days = models.CharField(blank=True, choices=DAYS)  # List of days of week
    active_months = models.Integer(blank=True, choices=MONTHS)  # List of Months
    active_date_begin = models.DateField(blank=True)
    active_date_end = models.DateField(blank=True)


    """ Job run status """
    # Datetime of the next run. Blank if no future runs scheduled.
    next_run = models.DateTimeField(blank=True)
    # Datetime of last run. Also shows that the last run completed.
    # create logic that if current time >= next_run and last_run < next run,
    # then the job needs to be run now.
    last_run = models.DateTimeField(blank=True)
    # Use job_running to make sure not to run the job if it's currently
    # running.  # Job currently running, true/false.
    job_running = models.BooleanField(default=False)
    # how many times the job has been run
    run_count = models.Integer(default=0)



class Akjobs(models.Model):
    pass
