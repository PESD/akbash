from django.db import models
# import api.jobs
# import bpm.jobs


class DayOfMonth(models.Model):
    "Day of the month."
    day = models.IntegerField(primary_key=True)
    def __str__(self):
        return str(self.day)


class DayOfWeek (models.Model):
    "Day of the week."
    day = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=9)
    def __str__(self):
        return self.name


class JobMonthlyDays(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    day = models.ForeignKey(DayOfMonth, on_delete=models.CASCADE)
    def __str__(self):
        if self.job and self.day:
            # return self.job.__str__() + " | " + self.day.__str__()
            return "Job " + str(self.job.id) + " Day " + str(self.day.day)


class JobWeeklyDays(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    day = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    def __str__(self):
        if self.job and self.day:
            return self.job.__str__() + " | " + self.day.__str__()


class Job(models.Model):
    "Job definition"


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
        help_text="Schedule a reoccuring job that runs every time " +
                  "interval. Ex., Run every 5 minutes. Submit a " +
                  "timedelta object. ex., datetime.timedelta(minutes=5)")


    # #### Monthly ####
    monthly_days = models.ManyToManyField(DayOfMonth, through=JobMonthlyDays)

    # TODO: Finish making this property. IM HERE
    #       Test with job id 9
    @property
    def monthly_days_list(self):
        days = []
        qs = DayOfMonth.objects.filter(job=self)
        for i in qs:
            days.append(i.day)
        if days:
            return days

    @monthly_days_list.setter
    def monthly_days_list(self, days):
        # delete days not in list
        JobMonthlyDays.objects.filter(job=self).exclude(day__in=days).delete()
        # add days from list
        for i in days:
            DOM = DayOfMonth.objects.get(day=i)
            JobMonthlyDays.objects.update_or_create(job=self, day=DOM)

    @monthly_days_list.deleter
    def monthly_days_list(self):
        JobMonthlyDays.objects.filter(job=self).delete()

    # TODO: make validation to check for date if run_monthly is set or fill in
    # default time if no time is given and run_monthly is set.
    run_monthly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the monthly / days of month jobs.")


    # #### Weekly ####
    # TODO: Change weekly to be like monthly above.
    # TODO: validation stuff, same as monthly
    run_weekly = models.CharField(
        max_length=21,
        null=True,
        blank=True,
        help_text="Comma seperated list of days of the week to run the job. " +
                  "Use integers for each day starting at 1 for Sunday, 2 for " +
                  "Monday, and so on to 7 for Saturday.")

    # TODO: same as monthly
    run_weekly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the weekly / days of week jobs.")

    """ Limit number of runs. """
    run_count_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Each time the job is run, the run count is incremented by " +
                  "1. You may set a limit to how many times the job runs. " +
                  "When the run count exceeds this value, the job is no " +
                  "longer scheduled to run.")

    """ Limit job run to a window of time. """
    # TODO: need validator to check for both dates.
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
    # TODO: need validator
    active_dow = models.CharField(
        max_length=21,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed days of week. " +
                  "Comma seperated list of days of the week. " +
                  "Use integers for each day starting at 1 for Sunday, 2 for" +
                  "Monday, and so on to 7 for Saturday.")
    # TODO: need validator
    active_days = models.CharField(
        max_length=124,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed days. Comma seperated list of " +
                  "days of the month to limit the job run times to. Ex., 1,15 " +
                  "means limit the run to the 1st and 15th of each month.")
    # TODO: need validator
    active_months = models.CharField(
        max_length=48,
        null=True,
        blank=True,
        help_text="Limit job runs to the listed months. Comma seperated list " +
                  "of integer months to limit the job run times to. " +
                  "1 for January, 2 for February, 12 for December.")
    # TODO: need validator to check for both dates
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
    # A generic enabled / disabled toggle so jobs can be paused
    job_enabled = models.BooleanField(default=True)


    """ The code to run
        I'm thinking of using two ways.
            1. Specify a callable to be ran. Limit to callables in a jobs
               module in each akjob app. Or maybe make a jobs package and
               modules in that package contain the code for the jobs.
            2. Submit a class instance object that will be serialized then
               stored then retreived and executed when the job is ran. Maybe
               standardize on a run() method that will be ran by akjob.
    """
    """
    # Maybe I should add command_argv or something like that.
    command = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="The callable object to be ran.")

    # Possibly install/use django-picklefield
    # pickled_cmd = PickledObjectField()
    # or do it yourself and put the picked object into a generic binary field.
    # pickled_cmd = models.BinaryField()
    """


    def __str__(self):
        if self.id and self.name:
            return str(self.id) + " - " + self.name
        elif self.id:
            return str(self.id)
        elif self.name:
            return "No id - " + self.name
        else:
            return "No id - No Name"


    """ Validate before saving.
        This does not apply to creating or updating objects in bulk. """
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Job, self).save(*args, **kwargs)
        # self.refresh_from_db()
        """ The only reason I reload from the DB, using self.refresh_from_db(),
            is I've been using pendulum a lot but when pendulum objects are
            saved they get turned into datetime objects. Reloading right away
            helps avoid errors by reminding me not to do special pendulum
            things unless you first turn the datetime objects to pendulum
            objects. """


""" Populate the DayOfMonth and DayOfWeek models
    https://docs.djangoproject.com/en/1.11/howto/initial-data/
    The data is loaded using fixtures but here are some function if you need to
    manually load the data.
"""
def load_DayOfMonth():
    for d in range(1, 32):
        DayOfMonth.objects.update_or_create(day=d)

# Using days 1-7 starting on Sunday because that's what the queryset field lookup
# week_day uses.
def load_DayOfWeek():
    DayOfWeek.objects.update_or_create(day=1, name="Sunday")
    DayOfWeek.objects.update_or_create(day=2, name="Monday")
    DayOfWeek.objects.update_or_create(day=3, name="Tuesday")
    DayOfWeek.objects.update_or_create(day=4, name="Wednesday")
    DayOfWeek.objects.update_or_create(day=5, name="Thursday")
    DayOfWeek.objects.update_or_create(day=6, name="Friday")
    DayOfWeek.objects.update_or_create(day=7, name="Saturday")
