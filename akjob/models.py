from datetime import datetime, timezone, timedelta
from django.db import models
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _
# import api.jobs
# import bpm.jobs


# It might be wrong for my list properties to have a deleter since
# deleting an attribute from a django model instance is a way of reloading that
# attribute from the database.


# I've been having terrible trouble trying to keep track of timezones. Many
# problems stem from MS SQL not being well supported by django. Between
# django-pyodbc-azure and pyodbc I'm guessing the bugs reside.
# models.TimeFields are not storing tzinfo though maybe thats because date
# is required to calculate timezone and dst stuff. So then I decided to use
# models.DurationField to store datetime.timedelta objects to be used as
# timezone offsets to create datetimes with. Turns out that negative
# timedeltas are not being stored correctly. So now I'm making a model field
# which you give a timedelta to and it converts it to seconds which are
# stored as an integer in the database.

class TimeZoneOffsetField(models.Field):
    """ This field takes a timedelta and stores it in the DB as seconds in an
        integer number field. """
    description = "Timezone offset expressed as a datetime.timedelta object."

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value is invalid. It should be a "
                     "datetime.timedelta object.")
    }

    # Store the data as an integer field in the DB.
    def get_internal_type(self):
        return "IntegerField"

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return timedelta(seconds=value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, timedelta):
            return value
        try:
            td = timedelta(seconds=int(value))
        except ValueError:
            pass
        else:
            if td is not None:
                return td

        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )

    def get_prep_value(self, value):
        if value is None:
            return None
        return int(value.total_seconds())

    # Use formfield from sibling class models.DurationField.
    def formfield(self, **kwargs):
        super(models.DurationField, self).formfield(**wkargs)


class DayOfMonth(models.Model):
    "Day of the month."
    day = models.IntegerField(
        primary_key=True,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(31)])
    def __str__(self):
        return str(self.day)


class DayOfWeek(models.Model):
    "Day of the week."
    day = models.IntegerField(
        primary_key=True,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(7)])
    weekday = models.IntegerField()
    name = models.CharField(max_length=9)
    def __str__(self):
        return self.name


class Months(models.Model):
    month = models.IntegerField(
        primary_key=True,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)])
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
        qs = self.dates.all()
        # I could probably use list comprehension for this. but I forgot how.
        # jobdates = [d.job_datetime for d in qs]
        jobdates = []
        for d in qs:
            jobdates.append(d.job_datetime)
        if jobdates:
            return jobdates

    @dates_list.setter
    def dates_list(self, jobdates):
        if isinstance(jobdates, datetime):
            jobdates = [jobdates]
        if isinstance(jobdates, (list, tuple)):
            for d in jobdates:
                if not isinstance(d, datetime):
                    raise TypeError("List may only contain datetimes")
        else:
            raise TypeError("Datetime or a list containing datetime values " +
                            "are required.")

        JobDates.objects.filter(job=self).delete()
        for d in jobdates:
            self.dates.create(job_datetime=d)

    @dates_list.deleter
    def dates_list(self):
        JobDates.objects.filter(job=self).delete()


    """ Schedule reoccuring jobs """
    run_every = models.DurationField(
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(
            timedelta(minutes=1),
            "Value must be 1 minute or greater.")],
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
        qs = self.monthly_days.all()
        # days = [i.day for i in qs]
        days = []
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

    monthly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the monthly / days of month jobs.")

    monthly_time_tz_offset_timedelta = TimeZoneOffsetField(
        blank=True,
        default=timedelta(0),
        help_text="Set this field with a timezone " +
                  "offset to use with monthly_time. If blank, UTC " +
                  "is assumed. Submit a datetime.timedelta object.")


    # ##### Weekly #####
    # Using a set of days of the week, the job will run on each of those days.
    # Use integers or DayOfWeek objects starting at 1 for Sunday, 2 for Monday,
    # and so on to 7 for Saturday.
    weekly_days = models.ManyToManyField(DayOfWeek)

    # alternate interface with the weekly days related set using a list
    @property
    def weekly_days_list(self):
        # days = [i.day for i in self.weekly_days.all()]
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

    weekly_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time of day to run the weekly / days of week jobs.")

    weekly_time_tz_offset_timedelta = TimeZoneOffsetField(
        blank=True,
        default=timedelta(0),
        help_text="Timezone offset to use with weekly_time. If blank, UTC " +
                  "is assumed. Submit a datetime.timedelta object.")


    """ A generic enabled / disabled toggle so jobs can be paused """
    job_enabled = models.BooleanField(default=True)

    """ Limit number of runs. """
    run_count_limit = models.IntegerField(
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(1)],
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
    active_time_tz_offset_timedelta = TimeZoneOffsetField(
        blank=True,
        default=timedelta(0),
        help_text="Timezone offset. If blank, UTC " +
                  "is assumed. Submit a datetime.timedelta object.")

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
        # days = [i.day for i in self.active_weekly_days.all()]
        qs = self.active_weekly_days.all()
        days = []
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
        # days = [i.day for i in self.active_monthly_days.all()]
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
        # months = [i.month for i in self.active_months.all()]
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


    # ##### Active Dates #####
    # Limit job runs to a date range
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
    _next_run = models.DateTimeField(null=True, blank=True)
    # Datetime of last run. Also shows that the last run completed.
    # create logic that if current time >= next_run and last_run < next run,
    # then the job needs to be run now.
    _last_run = models.DateTimeField(null=True, blank=True)
    # Use job_running to make sure not to run the job if it's currently
    # running.  # Job currently running, true/false.
    _job_running = models.BooleanField(default=False)
    # how many times the job has been run
    _run_count = models.IntegerField(default=0)
    # datetime of the last interval.
    # For use with run_every to help figure the next interval
    _last_interval = models.DateTimeField(null=True, blank=True)


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
        This does not apply to creating or updating objects in bulk or
        model.objects.create(), according to the docs. Turns out in my testing
        that some validations are ran during model.objects.create() with this
        setup.
    """
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Job, self).save(*args, **kwargs)


    """ More Field validations
    """
    def clean(self):

        # make sure both active_time_begin and active_time_end are set if any
        # one of them are set.
        if any((self.active_time_begin, self.active_time_end)):
            if not all((self.active_time_begin, self.active_time_end)):
                raise exceptions.ValidationError(
                    'If either active_time_begin or active_time_end are ' +
                    'set, both must be set.')
            if self.active_time_tz_offset_timedelta is None:
                raise exceptions.ValidationError(
                    'If active_time_[begin|end] is set, ' +
                    'active_time_tz_offset_timedelta must also be set.')

        # make sure both active_date_begin and active_date_end are set if any
        # one of them are set.
        if any((self.active_date_begin, self.active_date_end)):
            if not all((self.active_date_begin, self.active_date_end)):
                raise exceptions.ValidationError(
                    'If either active_date_begin or active_date_end are ' +
                    'set, both must be set.')

        # Relationships can't touched until self.id is created so some
        # validations will have to be skipped.
        if self.id is None:
            return

        # If there are monthly_days, make sure monthly_time and tz is set.
        # IDEA: Instead of raising an error, I could instead set a default time
        # such as datetime.now(). This might be a bad idea since this might not
        # run until way after the instance is created so unexpected times may
        # be used.
        if self.monthly_days.all():
            # if any return False then...
            if not any((self.monthly_time,
                        self.monthly_time_tz_offset_timedelta)):
                raise exceptions.ValidationError(
                    'If monthly_days is set, monthly_time and ' +
                    'monthly_time_tz_offset_timedelta must also be set.')

        if self.weekly_days.all():
            if not any((self.weekly_time,
                        self.weekly_time_tz_offset_timedelta)):
                raise exceptions.ValidationError(
                    'If weekly_days is set, weekly_time and ' +
                    'weekly_time_tz_offset_timedelta must also be set.')


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


    @staticmethod
    def dtfloormin(dt):
        "Returns datetime floored to minutes"
        return dt.replace(second=0, microsecond=0)


    def next_run(self):
        "Find the next run time."

        now = self.dtfloormin(datetime.now(tz=timezone.utc))
        # A variable to show what is causing a return of now.
        global run_now_set_by
        global run_datetimes
        # ### Build a dt list of run times. ###
        # a list to hold multiple times when jobs might run.
        jtimes = []

        # run_every intervals - This should be checked 1st.
        if self.run_every:
            if not self._last_interval:
                # I'm not sure if this is the right point to set _last_interval
                self._last_interval = now
                self.save()
                jtimes.append(now + self.run_every)
            elif self.dtfloormin(self._last_interval + self.run_every) <= now:
                # This job should run now
                run_now_set_by = "re"
                return now
            else:
                jtimes.append(self._last_interval + self.run_every)
        # check self.dates
        if self.dates.all():
            jtimes += self.dates_list
        # Monthly jobs
        if self.monthly_days.all():
            for d in self.monthly_days_list:
                # there is datetime.combine() but it doesn't help me that much
                # in this case.
                mdt = datetime(
                    now.year, now.month, d,
                    self.monthly_time.hour, self.monthly_time.minute,
                    tzinfo=timezone(self.monthly_time_tz_offset_timedelta))
                jtimes.append(mdt)
        # Weekly jobs
        qs = self.weekly_days.all()
        if qs:
            weekdaylist = [d.weekday for d in qs]
            for i in range(7):
                dt = now + timedelta(hours=24 * i)
                if dt.weekday() in weekdaylist:
                    dt.replace(hour=self.weekly_time.hour,
                               minute=self.weekly_time.minute,
                               tzinfo=timezone(
                                   self.weekly_time_tz_offset_timedelta))
                    jtimes.append(dt)
        # ### remove dt from jtimes if it falls outside of limits. ###
        if all((self.active_time_begin, self.active_time_end,
                self.active_time_tz_offset_timedelta is not None)):
            atb = self.active_time_begin.replace(
                second=0, microsecond=0,
                tzinfo=timezone(self.active_time_tz_offset_timedelta))
            ate = self.active_time_end.replace(
                second=0, microsecond=0,
                tzinfo=timezone(self.active_time_tz_offset_timedelta))
        awd = [d.weekday for d in self.active_weekly_days.all()]
        for i, v in enumerate(jtimes):
            if atb:
                t = v.time().replace(second=0, microsecond=0, tzinfo=v.tzinfo)
                if not atb <= t <= ate:
                    jtimes.pop(i)
                    continue
            if awd:
                if v.weekday() not in awd:
                    jtimes.pop(i)
                    continue
            if self.active_monthly_days.all():
                if v.day not in self.active_monthly_days_list:
                    jtimes.pop(i)
                    continue
            if self.active_months.all():
                if v.month not in self.active_months_list:
                    jtimes.pop(i)
                    continue
            if all((self.active_date_begin, self.active_date_end)):
                if not (self.active_date_begin <=
                        v.date() <=
                        self.active_date_end):
                    jtimes.pop(i)
                    continue
        # TODO: I"M HERE!!!
        # This method isn't working yet.
        jtimes.sort()

        # for debug
        from pprint import pprint
        pprint(jtimes)

        jtimes = [self.dtfloormin(t) for t in jtimes if self.dtfloormin(t) >= now]
        run_datetimes = jtimes.copy()
        # the list was sorted and datetimes in the past removed so this should
        # return the lowest (earliest) datetime.
        return jtimes[0]


    # the way the pieces are falling together, I may not need this.
    def isruntime(self):
        "Determine if this job should be ran now. Return True or False."
        pass


    def run(self):
        "Perform the job."
        now = self.dtfloormin(datetime.now(tz=timezone.utc))
        global run_now_set_by
        # do stuff and run the job then...
        self._job_running = False
        self._runcount += 1
        self._last_run = now
        if run_now_set_by == "re":
            self._last_interval = now
        self.save()


    # I didn't test this section well since it's not essential and time is
    # limited.
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

        print("\nThis job was last ran: " + str(self._last_run))
        print("This job's next schedule run time is: " + str(self._next_run))

        print("\nRun count: " + str(self._run_count))
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
            mdt = str(self.monthly_time.replace(
                tzinfo=timezone(self.monthly_time_tz_offset_timedelta)))
            print("\nMonthly jobs are ran at: " + mdt)

        if self.weekly_days.all():
            wd = True
            print("\nThis job is scheduled to run on the following days of " +
                  "the week:")
            for d in self.weekly_days.all():
                print("    " + d.name)
            wdt = str(self.weekly_time.replace(
                tzinfo=timezone(self.weekly_time_tz_offset_timedelta)))
            print("Weekly jobs are ran at: " + wdt)

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
            atb = str(self.active_time_begin.replace(
                tzinfo=timezone(self.active_time_tz_offset_timedelta)))
            ate = str(self.active_time_end.replace(
                tzinfo=timezone(self.active_time_tz_offset_timedelta)))
            iprint(atb + " to " + ate)
            if not self.active_time_end:
                iprint("This limit is not in effect since active_time_end is" +
                       " not set.")

        if self.active_monthly_days.all():
            print("\nThis job will not run outside of the following days of ",
                  "the month:")
            print("    ", end='')
            for d in self.active_monthly_days.all():
                print(str(d.day), end=' ')
            print()

        if self.active_weekly_days.all():
            print("\nThis job will not run outside of the following days of ",
                  "the week:")
            for d in self.active_weekly_days.all():
                print("    " + d.name)

        if self.active_months.all():
            print("\nThis job will not run outside of the following months:")
            for m in self.active_months.all():
                iprint(m.name)

        # for debug
        # global run_datetimes
        # print("\nList of run times:")
        # iprint(run_datetimes)

        print()



""" Populate the DayOfMonth and DayOfWeek models
    https://docs.djangoproject.com/en/1.11/howto/initial-data/
    The data may be loaded using the functions below or be loaded from the
    fixtures:
        python manage.py loaddata akjob_dayofweek.json akjob_dayofmonth.json
"""
def load_DayOfMonth():
    for d in range(1, 32):
        DayOfMonth.objects.create(day=d)

# Using days 1-7 starting on Sunday because that's what the queryset field
# lookup week_day uses and it makes sense to most Americans.
# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#week-day
# The weekday field matches with datetime.weekday().
def load_DayOfWeek():
    DayOfWeek.objects.create(day=1, weekday=6, name="Sunday")
    DayOfWeek.objects.create(day=2, weekday=0, name="Monday")
    DayOfWeek.objects.create(day=3, weekday=1, name="Tuesday")
    DayOfWeek.objects.create(day=4, weekday=2, name="Wednesday")
    DayOfWeek.objects.create(day=5, weekday=3, name="Thursday")
    DayOfWeek.objects.create(day=6, weekday=4, name="Friday")
    DayOfWeek.objects.create(day=7, weekday=5, name="Saturday")

def load_Months():
    Months.objects.create(month=1, name="January")
    Months.objects.create(month=2, name="February")
    Months.objects.create(month=3, name="March")
    Months.objects.create(month=4, name="April")
    Months.objects.create(month=5, name="May")
    Months.objects.create(month=6, name="June")
    Months.objects.create(month=7, name="July")
    Months.objects.create(month=8, name="August")
    Months.objects.create(month=9, name="September")
    Months.objects.create(month=10, name="October")
    Months.objects.create(month=11, name="November")
    Months.objects.create(month=12, name="December")
