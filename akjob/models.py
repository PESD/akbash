""" akjob models """
# import importlib
from akjob.akjob_logger import AkjobLogging
from datetime import datetime, timezone, timedelta
from django.db import models, transaction
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _
from picklefield.fields import PickledObjectField

""" Notes:

*** List Properties ***
It might be wrong for my list properties to have a deleter since deleting an
attribute from a django model instance is a way of reloading that attribute
from the database. The deleter is so much easier to use then deleting the
related rows that I want to keep the deleter.


*** TimeZoneOffsetField ***
I've been having terrible trouble trying to keep track of timezones. Many
problems stem from MS SQL not being well supported by django. Between
django-pyodbc-azure and pyodbc I'm guessing the bugs reside.  models.TimeFields
are not storing tzinfo though maybe thats because date is required to calculate
timezone and dst stuff. So then I decided to use models.DurationField to store
datetime.timedelta objects to be used as timezone offsets to create datetimes
with. Turns out that negative timedeltas are not being stored correctly. So now
I'm making a model field which you give a timedelta to and it converts it to
seconds which are stored as an integer in the database.

*** Ideas for future versions ***
Create an option for the job to delete itself when it goes inactive. This can
be done right now by including code to do that in the job_code_object so I'm
thinking a flag that could be turned on then the job would delete itself when
job is enabled but there are no future job runs scheduled.

Similar to monthly days, you could shedule hours. So you could schedule hourly
jobs but control when they run. For instance, run at the top of the hour.
Currently, you can schedule an interval using hours but you don't know at what
minute the job will run. This could be expanded furthor to make crontab like
scheduling.

Create a logging object that can be used by job code objects that won't be
detached when akjobd daemonizes.

Look into optimizing the interval/run_every jobs. They take a long time to
check each loop. Need to find a better way then adding 300 future datetimes.
"""



""" Set up logging
"""
# I should probably put this into a function?
models_logging = AkjobLogging(name="akjob.job",
                              logfilename="akjob.job.log",
                              format_str=AkjobLogging.multiline_format_str)
logger = models_logging.get_logger()



""" Custom fields
"""
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
        super(models.DurationField, self).formfield(**kwargs)


""" Relational models used by the main Job model.
"""
# This model is populated by a fixture and is basically used as a LOV. There's
# probably a better way to handle this that doesn't touch a database.
class DayOfMonth(models.Model):
    "Day of the month."
    day = models.IntegerField(
        primary_key=True,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(31)])
    def __str__(self):
        return str(self.day)


# This model is populated by a fixture
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


# This model is populated by a fixture
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


""" The main model that does most akjob stuff.
"""
class Job(models.Model):
    "Job definition"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Some misc tracking variables. A variable to show what is causing a
        # return of now job run time. A list of future job run times.
        self._run_now_set_by = None
        self._run_datetimes = None


    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default=None,  # Used to cause error if name isn't provided.
        unique=False,
        help_text="Name the job. Repeat names are allowed. Required Field.")


    """ Fields to store the job code to be ran. """
    # Field holding job code to run. Store an object with a run() method. The
    # object will be pickeled. See this documentation for details about
    # pickeling and unpickeling the objects.
    # docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled
    job_code_object = PickledObjectField(null=True, blank=True, default=None)

    # This isn't needed. I previouly thought the module containing the pickeled
    # object's type class needed to be imported.
    # job_code_object_module = models.CharField(
    #     max_length=96,
    #     null=True,
    #     blank=True)


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


    """ Schedule jobs on a monthly or weekly basis. """
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


    """ Limiting options
    """

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

    """ Limit job runs to specific days of the week. """
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


    """ Limit job runs to specific days of the month. """
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


    """ Limit job runs to specific months. """
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


    """ Limit job runs to specific dates. """
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


    """ Job run status
    """
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


    """ Delete me flag
        Setting deleteme to True will delete the job on the next run.
        Inside of job code objects, use this flag instead of the stardard ways
        to delete a job object.
    """
    deleteme = models.BooleanField(default=False)


    """ Delete job when run count limit reached
    """
    delete_on_run_count_limit = models.BooleanField(default=False)


    """ Specify a timeout in seconds. When the job is executing, if the timeout
        is reached, the job process will be terminated. Default timeout is 5
        minutes.
    """
    timeout = models.IntegerField(default=300)




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
        # Consider calling self.next_run() here except next_run calls save() so
        # will that make a loop. So it's more complicated.


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

        # Make sure there is a run_count_limit if delete_on_run_count_limit=T
        if self.delete_on_run_count_limit is True:
            if self.run_count_limit is None:
                raise exceptions.ValidationError(
                    'run_count_limit is not set while'
                    ' delete_on_run_count_limit is True. Eiter set a'
                    ' run_count_limit or set delete_on_run_count_limit to'
                    ' False.')

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


    @staticmethod
    def dtfloormin(dt):
        "Returns datetime floored to minutes"
        return dt.replace(second=0, microsecond=0)


    # TODO: More testing need to be done on this method.
    # FIXME: run_every job create outside run limits works correctly but will
    # appear as inactive in management command akjobd joblist and self.next_run
    # will be None. This could be confusing to the user. I don't have a good
    # solution to fix and it seems like a minor problem I might ignore?
    # Maybe create new method that will tell if a dt should not be included
    # because of set limits. Then you could iterate until the next dt if found.
    #
    # I'm thinking this should be split apart. A schedule_run method should be
    # created to schedule jobs then next_run will only return the dt of the
    # next run.
    def next_run(self, now=None):
        "Find the next run time."

        # Don't do anything if job is disabled, except set _next_run to None.
        if self.job_enabled is False:
            if self._next_run is not None:
                self._next_run = None
                self.save()
            return

        if now is None:
            now = self.dtfloormin(datetime.now(tz=timezone.utc))

        # ### Build a dt list of run times. ###
        # a list to hold multiple times when jobs might run.
        jtimes = []

        # run_every intervals - This should be checked 1st.
        if self.run_every:
            if not self._last_interval:
                self._last_interval = now
                self.save()
                jtimes.append(now + self.run_every)
                # print("append from run_every/no interval: ",  # debug
                #       str(now + self.run_every))  # debug
            elif self.dtfloormin(self._last_interval + self.run_every) <= now:
                # This job should run now
                self._run_now_set_by = "re"
                jtimes.append(now)
            # add in extra intervals in jtimes in case run limits are used.
            # Hopefully we can find a _next_run.
            for i in range(2, 301):
                jtimes.append(self._last_interval + self.run_every * i)
        # check self.dates
        if self.dates.all():
            jtimes += self.dates_list
        # Monthly jobs
        if self.monthly_days.all():
            for d in self.monthly_days_list:
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
                    dt = dt.replace(hour=self.weekly_time.hour,
                                    minute=self.weekly_time.minute,
                                    tzinfo=timezone(
                                        self.weekly_time_tz_offset_timedelta))
                    # print("append from weekly: ", str(dt))  # debug
                    jtimes.append(dt)
        # ### remove dt from jtimes if it falls outside of limits. ###
        atb, ate, awd = None, None, None
        if all((self.active_time_begin, self.active_time_end,
                self.active_time_tz_offset_timedelta is not None)):
            atb = self.active_time_begin.replace(
                second=0, microsecond=0,
                tzinfo=timezone(self.active_time_tz_offset_timedelta))
            ate = self.active_time_end.replace(
                second=0, microsecond=0,
                tzinfo=timezone(self.active_time_tz_offset_timedelta))
        awd = [d.weekday for d in self.active_weekly_days.all()]
        # print(jtimes)  # for debug
        # logger.debug(jtimes)  # for debug
        jtimes_copy = jtimes.copy()
        for v in jtimes_copy:
            if atb:
                t = v.time().replace(second=0, microsecond=0, tzinfo=v.tzinfo)
                # print("t =", t)  # debug
                if not atb <= t < ate:
                    # print("active time:", str(jtimes.count(v)), str(v))  # debug
                    for i in range(jtimes.count(v)):
                        jtimes.remove(v)
                    continue
            if awd:
                if v.weekday() not in awd:
                    # print("weekly:", str(jtimes.count(v)), str(v))  # debug
                    for i in range(jtimes.count(v)):
                        jtimes.remove(v)
                    continue
            if self.active_monthly_days.all():
                if v.day not in self.active_monthly_days_list:
                    # print("monthly:", str(jtimes.count(v)), str(v))  # debug
                    for i in range(jtimes.count(v)):
                        jtimes.remove(v)
                    continue
            if self.active_months.all():
                if v.month not in self.active_months_list:
                    # print("months:", str(jtimes.count(v)), str(v))  # debug
                    for i in range(jtimes.count(v)):
                        jtimes.remove(v)
                    continue
            if all((self.active_date_begin, self.active_date_end)):
                if not (self.active_date_begin <=
                        v.date() <=
                        self.active_date_end):
                    # print("active dates:", str(jtimes.count(v)), str(v))  # debug
                    for i in range(jtimes.count(v)):
                        jtimes.remove(v)
                    continue
        # print(jtimes)  # for debug
        # print()  # for debug
        # logger.debug(jtimes)  # for debug
        if not jtimes:
            if self._next_run is not None:
                self._next_run = None
                self.save()
            return None
        jtimes.sort()
        jtimes = [self.dtfloormin(t) for t in jtimes if self.dtfloormin(t) >= now]
        if not jtimes:
            if self._next_run is not None:
                self._next_run = None
                self.save()
            return None
        # Done with _run_datetimes at this point. This is for debug.
        self._run_datetimes = jtimes.copy()
        # the list was sorted and datetimes in the past removed so this should
        # return the lowest (earliest) datetime.
        self._next_run = jtimes[0]
        self.save()
        return jtimes[0]


    # Because new jobs are not scheduled when created the user may want to
    # want to manually get the job scheduled right away by calling the next_run
    # method. I'm creating this alias as schedule_run is easier to remember and
    # makes more sense to the user.
    schedule_run = next_run


    # TODO: This needs testing.
    def isruntime(self):
        "Determine if this job should be ran now. Return True or False."

        now = self.dtfloormin(datetime.now(tz=timezone.utc))

        # akjobd filters out disabled jobs so this block isn't used often.
        # Return False if job is disabled.
        if self.job_enabled is False:
            if self._next_run is not None:
                self._next_run = None
                self.save()
            logger.info("Job <" + str(self) + ">: Job disabled.")
            return False

        # akjobd filters out jobs passed the count limit so this block isn't
        # used often.
        # If run limit is reached, return false
        if self.run_count_limit:
            if self._run_count >= self.run_count_limit:
                if self._next_run is not None:
                    self._next_run = None
                    self.save()
                logger.info("Job <" + str(self) + ">: Job count " +
                            "limit reached.")
                return False

        # Run next_run() and return false if it doesn't return a value.
        next_run = self.next_run(now=now)
        if next_run is None:
            return False

        # check if the job should run now.
        now = self.dtfloormin(datetime.now(tz=timezone.utc))
        if now >= next_run:
            if self._last_run is None:
                return True
            if self._last_run < next_run:
                return True
        else:
            return False


    def execute(self):
        "Execute the job code."

        # Pre run
        run_now_set_by = None
        if self._run_now_set_by == "re":
            run_now_set_by = "re"
            self._run_now_set_by = None
        self._job_running = True
        self.save()

        # This is not needed. Import module
        # if self.job_code_object_module:
        #     logger.debug("Attempting to load module " +
        #                  self.job_code_object_module)
        #     importlib.import_module(self.job_code_object_module)

        # run
        logger.debug("Attempting to run job <" + str(self) + ">")
        code = self.job_code_object
        try:
            code.run(ownjob=self)
        except Exception as inst:
            logger.error("Something went wrong with Job " + str(self.id) +
                         ", " + self.name + "\n    " + str(inst))
        else:
            logger.debug("Finished running job <" + str(self) + ">")

        # Post run
        self._job_running = False
        self._run_count += 1
        self._last_run = datetime.now(timezone.utc)
        if run_now_set_by == "re":
            self._last_interval = datetime.now(timezone.utc)
        self.save()


    def run(self):
        "Check if job should be ran now. If so, perform the job."

        # Return if the job shouldn't be ran now.
        if self.isruntime() is False:
            logger.debug("Job <" + str(self) + "> not running at this time.")
            return

        # Return if _job_running flag. I have a worry of jobs crashing before
        # completion and the _job_running flag never being set back to False.
        if self._job_running is True:
            logger.info("Job <" + str(self) + "> didn't run because job " +
                        "running flag is True.")
            return

        # Return if there is no job code to run.
        if self.job_code_object is None:
            logger.warn("Job <" + str(self) + ">: No job code ran. " +
                        "job_code_object is None.")
            return

        # Execute Job
        self.execute()


    # This should probably be called something else. maybe print_info()?
    # I didn't test this section well since it's not essential and time is
    # limited.
    def print(self):  # noqa  -  Problems with Rob's linter.
        "Display (pretty print) the job's defined values."
        from textwrap import TextWrapper
        from pprint import pprint

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
            print("\nThis job will not run outside of the following days of",
                  "the month:")
            print("    ", end='')
            for d in self.active_monthly_days.all():
                print(str(d.day), end=' ')
            print()

        if self.active_weekly_days.all():
            print("\nThis job will not run outside of the following days of",
                  "the week:")
            for d in self.active_weekly_days.all():
                print("    " + d.name)

        if self.active_months.all():
            print("\nThis job will not run outside of the following months:")
            for m in self.active_months.all():
                iprint(m.name)

        # This is not saved in the model so this will rarely be set.
        if self._run_datetimes:
            print("\nList of run times:")
            pprint(self._run_datetimes)

        print("\nCurrent datetime: " + str(datetime.now(timezone.utc)))
        print()


class JobCallable():
    "Used to create job objects given a callable and argv."

    def __init__(self, callable_object, *args, **kwargs):
        self.callable_object = callable_object
        self.args = args
        self.kwargs = kwargs

    def run(self, ownjob=None):
        self.callable_object(*self.args, **self.kwargs)

    # Might as well make this callable since "callable" is in the name.
    def __call__(self):
        self.run()


""" Some utility fuctions used by the akjobd management command and possibly
    else where.
"""
def list_jobs():
    active_job_list = []
    inactive_job_list = []
    for j in Job.objects.all():
        if j.next_run():
            active_job_list.append(j)
        else:
            inactive_job_list.append(j)
    print("Active jobs:")
    if active_job_list:
        for j in active_job_list:
            print("    Job {} | {} | {}".format(
                str(j.id), str(j._next_run), j.name))
    else:
        print("    None")
    print("Inactive jobs:")
    if inactive_job_list:
        for j in inactive_job_list:
            print("    Job {0} | {1:32} | {2}".format(
                str(j.id),
                j.name,
                "Job enabled: " + str(j.job_enabled)))
    else:
        print("    None")


def job_exists(idnum):
    try:
        Job.objects.get(id=idnum)
        return True
    except Job.DoesNotExist:
        return False


def enable_job(idnum):
    j = Job.objects.get(id=idnum)
    j.job_enabled = True
    logger.info("Setting job_enabled to True. Job: " + j.__str__())
    j.save()


def disable_job(idnum):
    j = Job.objects.get(id=idnum)
    j.job_enabled = False
    logger.info("Setting job_enabled to False. Job: " + j.__str__())
    j.save()


def delete_job(idnum):
    j = Job.objects.get(id=idnum)
    logger.info("Deleting job: " + j.__str__())
    Job.objects.filter(id=idnum).delete()


""" Populate the DayOfMonth and DayOfWeek models
    https://docs.djangoproject.com/en/1.11/howto/initial-data/
    The data may be loaded using the functions below or be loaded from the
    fixtures:
        python manage.py loaddata akjob_dayofweek.json akjob_dayofmonth.json \
        akjob_months.json
"""
@transaction.atomic
def load_DayOfMonth(refresh=False):
    if refresh is True:
        logger.info("Reloading DayOfMonth")
        DayOfMonth.objects.all().delete()
    for d in range(1, 32):
        DayOfMonth.objects.create(day=d)

# Using days 1-7 starting on Sunday because that's what the queryset field
# lookup week_day uses and it makes sense to most Americans.
# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#week-day
# The weekday field matches with datetime.weekday().
@transaction.atomic
def load_DayOfWeek(refresh=False):
    if refresh is True:
        logger.info("Reloading DayOfWeek")
        DayOfWeek.objects.all().delete()
    DayOfWeek.objects.create(day=1, weekday=6, name="Sunday")
    DayOfWeek.objects.create(day=2, weekday=0, name="Monday")
    DayOfWeek.objects.create(day=3, weekday=1, name="Tuesday")
    DayOfWeek.objects.create(day=4, weekday=2, name="Wednesday")
    DayOfWeek.objects.create(day=5, weekday=3, name="Thursday")
    DayOfWeek.objects.create(day=6, weekday=4, name="Friday")
    DayOfWeek.objects.create(day=7, weekday=5, name="Saturday")

@transaction.atomic
def load_Months(refresh=False):
    if refresh is True:
        logger.info("Reloading Months")
        Months.objects.all().delete()
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
