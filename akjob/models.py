from datetime import datetime, timezone
from django.db import models
# import api.jobs
# import bpm.jobs


class DayOfMonth(models.Model):
    "Day of the month."
    day = models.IntegerField(primary_key=True)
    def __str__(self):
        return str(self.day)


class DayOfWeek(models.Model):
    "Day of the week."
    day = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=9)
    def __str__(self):
        return self.name


class Months(models.Model):
    month = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=9)
    def __str__(self):
        return self.name


# So it could be confusing naming the foreign key manager "dates" (the
# related_name) and using other variables named "jobdates" as that makes things
# totally backwards but I think naming the manager "dates" creates a nice,
# easier to understand interface for the users of the Job model.
class JobDates(models.Model):
    "Jobs and dates (datetimes) they're scheduled to run."
    job = models.ForeignKey(
        "Job",
        on_delete=models.CASCADE,
        related_name='dates')
    job_datetime = models.DateTimeField()
    def __str__(self):
        return "Job " + str(self.job.id) + " -> " + str(self.job_datetime)


class Job(models.Model):
    "Job definition"


    name = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        default=None,  # Used to cause error if name isn't provided.
        unique=False,
        help_text="Name the job. Repeat names are allowed. Required Field.")


    """ Schedule job to run at specific datetimes. """
    # Working in reverse direction with the foreign key manager sucks. here
    # are properties as an alternate method for setting dates.
    @property
    def dates_list(self):
        jobdates = []
        qs = self.dates.all()
        # I could probably use list comprehension for this. but I forgot how.
        for d in qs:
            jobdates.append(d.job_datetime)
        if jobdates:
            return jobdates

    @dates_list.setter
    def dates_list(self, jobdates):
        if isinstance(jobdates, datetime):
            JobDates.objects.filter(job=self).delete()
            self.dates.create(job_datetime=jobdates)
            return self.dates.all()
        elif isinstance(jobdates, (list, tuple)):
            for d in jobdates:
                if not isinstance(d, datetime):
                    raise TypeError("List may only contain datetimes")
        else:
            raise TypeError("Datetime or a list containing datetime values " +
                            "are required.")

        JobDates.objects.filter(job=self).delete()
        for d in jobdates:
            self.dates.create(job_datetime=d)
        return self.dates.all()

    @dates_list.deleter
    def dates_list(self):
        JobDates.objects.filter(job=self).delete()


    """ Schedule reoccuring jobs """
    # TODO: make a validation to only allow positive duration.
    run_every = models.DurationField(
        null=True,
        blank=True,
        help_text="Schedule a reoccuring job that runs every time " +
                  "interval. Ex., Run every 5 minutes. Submit a " +
                  "timedelta object. ex., datetime.timedelta(minutes=5)")


    # ##### Monthly #####
    # Using a set of days of the month, the job will run on each of those days.
    monthly_days = models.ManyToManyField(DayOfMonth)

    # Working with the relational manager is great in this case but I'm making
    # properties anyway since it fits my original vision of using a list.
    @property
    def monthly_days_list(self):
        days = []
        qs = self.monthly_days.all()
        for i in qs:
            days.append(i.day)
        if days:
            return days

    # WARNING: list methods do not fire off the setter. so
    #   Job().monthly_days_list.append(9) does nothing.
    @monthly_days_list.setter
    def monthly_days_list(self, days):
        if isinstance(days, (int, DayOfMonth)):
            self.monthly_days.set([days])
        elif isinstance(days, (list, tuple)):
            for d in days:
                if not isinstance(d, (int, DayOfMonth)):
                    raise TypeError("List may only contain integers and " +
                                    "DayOfMonth instances")
            self.monthly_days.set(days)
        else:
            raise TypeError("List, integer, or DayOfMonth instance required.")

    @monthly_days_list.deleter
    def monthly_days_list(self):
        self.monthly_days.clear()

    # TODO: make validation to check for date if monthly_days is set or fill in
    #       default time if no time is given and run_monthly is set.
    #       Also check for timezone. Assume utc if no timezone
    monthly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the monthly / days of month jobs.")


    # ##### Weekly #####
    # Using a set of days of the week, the job will run on each of those days.
    # Use integers or DayOfWeek objects starting at 1 for Sunday, 2 for Monday,
    # and so on to 7 for Saturday.
    weekly_days = models.ManyToManyField(DayOfWeek)

    # alternate interface with the weekly days related set using a list
    @property
    def weekly_days_list(self):
        days = []
        qs = self.weekly_days.all()
        for i in qs:
            days.append(i.day)
        if days:
            return days

    # WARNING: list methods do not fire off the setter. so
    #   Job().weekly_days_list.append(9) does nothing.
    @weekly_days_list.setter
    def weekly_days_list(self, days):
        if isinstance(days, (int, DayOfWeek)):
            self.weekly_days.set([days])
        elif isinstance(days, (list, tuple)):
            for d in days:
                if not isinstance(d, (int, DayOfWeek)):
                    raise TypeError("List may only contain integers and " +
                                    "DayOfWeek instances")
            self.weekly_days.set(days)
        else:
            raise TypeError("List, integer, or DayOfWeek instance required.")

    @weekly_days_list.deleter
    def weekly_days_list(self):
        self.weekly_days.clear()

    # TODO: same as monthly - Validation stuff. timezone stuff
    weekly_time = models.TimeField(
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

    # ##### Active Days Of Week #####
    # Limit job runs to the given days of week. Use integers or DayOfWeek
    # objects for each day starting at 1 for Sunday, 2 for Monday, and so on to
    # 7 for Saturday.
    active_weekly_days = models.ManyToManyField(
        DayOfWeek,
        related_name='ActiveDayOfWeek')

    # alternate interface with the weekly days related set using a list
    @property
    def active_weekly_days_list(self):
        days = []
        qs = self.active_weekly_days.all()
        for i in qs:
            days.append(i.day)
        if days:
            return days

    # WARNING: list methods do not fire off the setter. so
    #   Job().active_weekly_days_list.append(9) does nothing.
    @active_weekly_days_list.setter
    def active_weekly_days_list(self, days):
        if isinstance(days, (int, DayOfWeek)):
            self.active_weekly_days.set([days])
        elif isinstance(days, (list, tuple)):
            for d in days:
                if not isinstance(d, (int, DayOfWeek)):
                    raise TypeError("List may only contain integers and " +
                                    "DayOfWeek instances")
            self.active_weekly_days.set(days)
        else:
            raise TypeError("List, integer, or DayOfWeek instance required.")

    @active_weekly_days_list.deleter
    def active_weekly_days_list(self):
        self.active_weekly_days.clear()


    # ##### Active Days Of Month #####
    # Limit job runs to the given days of the month. Use integers or DayOfMonth
    # objects for each day you want to limit activity to. Ex., 1,15 means limit
    # the run to the 1st and 15th of each month.
    active_monthly_days = models.ManyToManyField(
        DayOfMonth,
        related_name='ActiveDayOfMonth')

    @property
    def active_monthly_days_list(self):
        days = []
        qs = self.active_monthly_days.all()
        for i in qs:
            days.append(i.day)
        if days:
            return days

    # WARNING: list methods do not fire off the setter. so
    #   Job().active_monthly_days_list.append(9) does nothing.
    @active_monthly_days_list.setter
    def active_monthly_days_list(self, days):
        if isinstance(days, (int, DayOfMonth)):
            self.active_monthly_days.set([days])
        elif isinstance(days, (list, tuple)):
            for d in days:
                if not isinstance(d, (int, DayOfMonth)):
                    raise TypeError("List may only contain integers and " +
                                    "DayOfMonth instances")
            self.active_monthly_days.set(days)
        else:
            raise TypeError("List, integer, or DayOfMonth instance required.")

    @active_monthly_days_list.deleter
    def active_monthly_days_list(self):
        self.active_monthly_days.clear()


    # ##### Active Months #####
    # Limit job runs to the given months. Use integers to represent which
    # months to limit the job run to. 1 for January, 2 for February, 12 for
    # December.
    active_months = models.ManyToManyField(Months)

    @property
    def active_months_list(self):
        months = []
        qs = self.active_months.all()
        for i in qs:
            months.append(i.month)
        if months:
            return months

    # WARNING: list methods do not fire off the setter. so
    #   Job().active_months_list.append(9) does nothing.
    @active_months_list.setter
    def active_months_list(self, months):
        if isinstance(months, (int, Months)):
            self.active_months.set([months])
        elif isinstance(months, (list, tuple)):
            for m in months:
                if not isinstance(m, (int, Months)):
                    raise TypeError("List may only contain integers and " +
                                    "Months instances")
            self.active_months.set(months)
        else:
            raise TypeError("List, integer, or Months instance required.")

    @active_months_list.deleter
    def active_months_list(self):
        self.active_months.clear()


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


    # TODO: I didn't test this section well since it's not essential and I have
    #       other stuff I need to do.
    def print(self):
        "Display (pretty print) the job's defined values."
        from textwrap import TextWrapper

        def wprint(*args):
            print(TextWrapper().fill(*args))

        def iprint(*args):
            print(TextWrapper(initial_indent="    ",
                              subsequent_indent="    ").fill(*args))

        print()
        wprint(self.name)

        if not self.job_enabled:
            print("\n***** This job is currently disabled *****")

        print("\nThis job was last ran: " + str(self.last_run))
        print("This job's next schedule run time is: " + str(self.next_run))

        print("\nRun count: " + str(self.run_count))
        if self.run_count_limit:
            print("Run count limit: " + str(self.run_count_limit))

        qs = self.dates.filter(
            job_datetime__gte=datetime.now(tz=timezone.utc))
        if qs:
            st = True
            print("\nThis job is scheduled to run at the following times:")
            for d in qs:
                iprint(str(d.job_datetime))
        qs = self.dates.filter(
            job_datetime__lt=datetime.now(tz=timezone.utc))
        if qs:
            st = True
            print("\nThe following scheduled times have already passed:")
            for d in qs:
                iprint(str(d.job_datetime))

        # I think I could format this better but I don't have time right now.
        if self.run_every:
            re = True
            print("\nThis job is a reoccuring job that runs every: ", end='')
            print(self.run_every)

        # I think I could format this better but I don't have time right now.
        if self.monthly_days.all():
            md = True
            print("\nThis job is scheduled to run on the following days of " +
                  "the month:")
            print("    ", end='')
            for d in self.monthly_days.all():
                print(str(d.day), end=' ')
            print("\nMontly jobs are ran at: " + str(self.monthly_time))

        if self.weekly_days.all():
            wd = True
            print("\nThis job is scheduled to run on the following days of " +
                  "the week:")
            for d in self.weekly_days.all():
                print("    " + d.name)
            print("Weekly jobs are ran at: " + str(self.weekly_time))

        if self.active_date_begin:
            print("\nThis job will not run outside the following date range:")
            iprint(str(self.active_date_begin) + " to " +
                   str(self.active_date_end))
            if not self.active_date_end:
                iprint("This limit is not in effect since active_date_end is" +
                       " not set.")

        if self.active_time_begin:
            print("\nThis job will not run outside the following time " +
                  "range, each day;")
            iprint(str(self.active_time_begin) + " to " +
                   str(self.active_time_end))
            if not self.active_time_end:
                iprint("This limit is not in effect since active_time_end is" +
                       " not set.")

        if self.active_monthly_days.all():
            print("\nThis job will not run on the following doays of the" +
                  " month:")
            print("    ", end='')
            for d in self.active_monthly_days.all():
                print(str(d.day), end=' ')
            print()

        if self.active_weekly_days.all():
            print("\nThis job will not run on the following days of the week:")
            for d in self.active_weekly_days.all():
                print("    " + d.name)

        if self.active_months.all():
            print("\nThis job will not run during the following months:")
            for m in self.active_months.all():
                iprint(m.name)

        print()


""" Populate the DayOfMonth and DayOfWeek models
    https://docs.djangoproject.com/en/1.11/howto/initial-data/
    The data may be loaded using the functions below or be loaded from the
    fixtures:
        python manage.py loaddata akjob_dayofweek.json akjob_dayofmonth.json
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

def load_Months():
    Months.objects.update_or_create(month=1, name="January")
    Months.objects.update_or_create(month=2, name="February")
    Months.objects.update_or_create(month=3, name="March")
    Months.objects.update_or_create(month=4, name="April")
    Months.objects.update_or_create(month=5, name="May")
    Months.objects.update_or_create(month=6, name="June")
    Months.objects.update_or_create(month=7, name="July")
    Months.objects.update_or_create(month=8, name="August")
    Months.objects.update_or_create(month=9, name="September")
    Months.objects.update_or_create(month=10, name="October")
    Months.objects.update_or_create(month=11, name="November")
    Months.objects.update_or_create(month=12, name="December")
