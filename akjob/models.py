import pendulum
from django.db import models

""" I thought I needed these for field "choices" options. Don't need them.
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
"""

class Job(models.Model):
    "Job definitions"


    name = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        default=None,  # Used to cause error if name isn't provided.
        unique=False,
        help_text="Name the job. Repeat names are allowed. Required Field.")


    """ Schedule One off job """
    run_once_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time to run the job.")

    """ Schedule reoccuring jobs """
    # TODO: make a validation to only allow positive duration.
    run_every = models.DurationField(
        null=True,
        blank=True,
        help_text="Run every ___. Format: [DD] [HH:[MM:]]ss. Schedule the job" +
                  "to repeatedly run after a time interval. Ex., Run every" +
                  "05:00 (5 minutes)")
    run_monthly = models.CharField(
        max_length=124,
        null=True,
        blank=True,
        help_text="Comma seperated list of days of the month to run the job." +
                  " Ex., 1,15 means run on the 1st and 15th of each month.")
    run_monthly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the monthly / days of month jobs.")
    run_weekly = models.CharField(
        max_length=21,
        null=True,
        blank=True,
        help_text="Comma seperated list of days of the week to run the job. " +
                  "Use integers for each day starting at 0 for Sunday, 1 for " +
                  "Monday, and so on to 6 for Saturday.")
    run_weekly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the weekly / days of week jobs.")
    run_count_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Each time the job is run, the run count is incremented by " +
                  "1. You may set a limit to how many times the job runs. " +
                  "When the run count exceeds this value, the job is no " +
                  "longer scheduled to run.")

    """ Limit job run to a window of time. """
    active_time_begin = models.TimeField(
        null=True,
        blank=True,
        help_text="Limit job runs to a time of day window between " +
                  "active_time_begin and active_time_end.")
    active_time_end = models.TimeField(
        null=True,
        blank=True,
        help_text="Limit job runs to a time of day window between " +
                  "active_time_begin and active_time_end.")
    active_dow = models.CharField(
        max_length=21,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed days of week. " +
                  "Comma seperated list of days of the week. " +
                  "Use integers for each day starting at 0 for Sunday, 1 for" +
                  "Monday, and so on to 6 for Saturday.")
    active_days = models.CharField(
        max_length=124,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed days. Comma seperated list of " +
                  "days of the month to limit the job run times to. Ex., 1,15 " +
                  "means limit the run to the 1st and 15th of each month.")
    active_months = models.CharField(
        max_length=48,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed months. Comma seperated list " +
                  "of integer months to limit the job run times to. " +
                  "1 for January, 2 for February, 12 for December.")
    active_date_begin = models.DateField(
        null=True,
        blank=True,
        help_text="Limit job runs times to the dates between " +
                  "active_date_begin and active_date_end.")
    active_date_end = models.DateField(
        null=True,
        blank=True,
        help_text="Limit job runs times to the dates between " +
                  "active_date_begin and active_date_end.")


    """ Job run status """
    # Datetime of the next run. Blank if no future runs scheduled.
    next_run = models.DateTimeField(null=True, blank=True)
    # Datetime of last run. Also shows that the last run completed.
    # create logic that if current time >= next_run and last_run < next run,
    # then the job needs to be run now.
    last_run = models.DateTimeField(null=True, blank=True)
    # Use job_running to make sure not to run the job if it's currently
    # running.  # Job currently running, true/false.
    job_running = models.BooleanField(default=False)
    # how many times the job has been run
    run_count = models.IntegerField(default=0)


    def __str__(self):
        if self.id and self.name:
            return str(self.id) + " - " + self.name
        elif self.id:
            return str(self.id)
        elif self.name:
            return "No id - " + self.name
        else:
            return "No id - Unsaved Job"


    """ Shortcuts to pendulum """
    interval = pendulum.interval
    datetime = pendulum.Pendulum
    dtcreate = pendulum.create
    now = pendulum.now
    timezone = pendulum.timezone




# class Akjobs(models.Model):
#     pass
