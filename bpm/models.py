from datetime import date, datetime, timedelta
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from akjob.models import Job, JobCallable
from api.models import Person, Employee, Position, Location, update_field
from api import ldap
# from api import visions
from django.contrib.auth.models import User
from bpm.visions_helper import VisionsHelper
from bpm.synergy_helper import SynergyHelper


# This is the Observer class. It is created when a task of the "Observer" type
# is activated.  This object is sent to a newly created Akjob Job as the code
# to be run.

class Observer:

    def __init__(self, job_id, workflow_task_id):
        self.job_id = job_id
        self.workflow_task_id = workflow_task_id

    def run(self, ownjob):
        workflow_task = WorkflowTask.objects.get(pk=self.workflow_task_id)
        # job = Job.objects.get(pk=self.job_id)
        args = {
            "workflow_task": workflow_task,
            "username": "tandem",
            "status": True,
        }
        # Do more stuff here.
        status, message = workflow_task.run_task(args)
        if status:
            ownjob.job_enabled = False
            ownjob.deleteme = True
            ownjob.save()
        return (status, message)


# A Process is something like "New Hire Process"
# A Process is a a set of Activities
# A Process defines a start_activity.
# Activities are one or more Tasks
# Activities define child Activities that come after that Activity is performed.
# A Workflow is a Process paired with a Person
# A Workflow (Process: New Hire, Person: Jon Snow) would start Jon Snow down /
# / the new hire process.
# WorkflowActivities keep track of each Workflow's Activity status
# -----
# Tasks store a function name. That function name can be accessed through /
# / the TaskWorker class. It uses **kwargs to accept any number of function args
# It is up to whatever is calling that function to know what args it needs to pass


class ProcessCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)


class Process(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(ProcessCategory)
    start_activity = models.ForeignKey(
        "Activity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    # All new Workflows start here. Starts a Workflow for this process and the
    # assigned person.  This generates a badge number (if needed), checks to
    # make sure there's no other Workflows active for this person, and creates
    # all of the WorkflowActivities and WorkflowTasks. It also sets the current
    # workflow field for the Person.

    def start_workflow(self, person):
        if person.current_workflow and self.name != "Cancel Workflow Process":
            return (False, "Finish or cancel current workflow before starting new one.")
        workflow = Workflow.objects.create(person=person, process=self)
        if not person.badge_number:
            person.generate_badge()
        person.status = "inprocess"
        if self.name == "Cancel Workflow Process":
            person.cancel_workflow = workflow
        else:
            person.current_workflow = workflow
        person.save()
        activities = self.activities.all()
        for activity in activities:
            workflow_activity = workflow.create_workflow_activity(activity)
            if activity == self.start_activity:
                workflow_activity.set_workflow_activity_active()
                workflow_activity.start_tasks()
        return (True, "Workflow successfully created.")


class Task(models.Model):
    TASK_TYPES = (
        ("System", "System"),
        ("Observer", "Observer"),
        ("User", "User"),
    )
    name = models.CharField(max_length=255)
    task_function = models.CharField(max_length=255)
    task_type = models.CharField(max_length=9, choices=TASK_TYPES)

    def task_controller_function(self, args):
        return getattr(TaskWorker, self.task_function)(**args)


class Activity(models.Model):
    name = models.CharField(max_length=255)
    children = models.ManyToManyField("Activity")
    tasks = models.ManyToManyField(Task)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="activities")
    users = models.ManyToManyField(User)


class Workflow(models.Model):
    STATUSES = (
        ("Complete", "Complete"),
        ("Error", "Error"),
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Canceled", "Canceled"),
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUSES, default="Active")
    jobs = models.ManyToManyField(Job)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="workflow_created_user")
    created_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="workflow_completed_user")
    completed_date = models.DateTimeField(null=True, blank=True)

    def cancel_all_jobs(self):
        self.jobs.all().delete()
        self.save()

    def cancel_workflow(self):
        self.cancel_all_jobs()
        self.status = "Canceled"
        self.save()
        wfas = self.workflow_activites.all()
        for wfa in wfas:
            wfa.status = "Canceled"
            wfa.save()

    def get_current_workflow_activities(self):
        return self.workflow_activites.filter(status="Active")

    def create_workflow_activity(self, activity):
        workflow_activity = WorkflowActivity.objects.create(workflow=self, activity=activity, status="Inactive")
        workflow_activity.create_workflow_tasks()
        return workflow_activity

    def check_for_completeness(self):
        workflow_activites = self.workflow_activites.exclude(status="Canceled")
        for workflow_activity in workflow_activites:
            if workflow_activity.status != "Complete":
                return False
        self.status = "Complete"
        self.save()
        self.cancel_all_jobs()
        if self.process.name == "Termination Process":
            self.person.status = "inactive"
        else:
            self.person.status = "active"
        self.person.current_workflow = None
        self.person.cancel_workflow = None
        self.person.save()
        return True


class WorkflowTask(models.Model):
    STATUSES = (
        ("Not Started", "Not Started"),
        ("Running", "Running"),
        ("Waiting", "Waiting"),
        ("Error", "Error"),
        ("Complete", "Complete"),
        ("Canceled", "Canceled"),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUSES)

    def run_task(self, args):
        status, message = self.task.task_controller_function(args)
        if status:
            user = None
            if "username" in args:
                try:
                    user = User.objects.get(username=args["username"])
                except ObjectDoesNotExist:
                    user = None
            self.status = "Complete"
            self.save()
            self.advance_activities(user)
        else:
            self.status = "Error"
            self.save()
        return (status, message)

    def advance_activities(self, user=None):
        workflow_activities = self.workflowactivity_set.all()
        for workflow_activity in workflow_activities:
            workflow_activity.advance_workflow_activity(user)

    def add_job_to_workflow(self, job):
        wfas = self.workflowactivity_set.all()
        for wfa in wfas:
            wfa.workflow.jobs.add(job)

    def start_observer(self, minutes, args):
        workflow_task = args["workflow_task"]
        job = Job.objects.create(name=self.task.name)
        code = Observer(job.id, workflow_task.id)
        job.job_code_object = code
        job.run_every = timedelta(minutes=minutes)
        job.save()
        self.add_job_to_workflow(job)


class WorkflowActivity(models.Model):
    STATUSES = (
        ("Complete", "Complete"),
        ("Error", "Error"),
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Next", "Next"),
        ("Canceled", "Canceled"),
    )
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="workflow_activites")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUSES)
    workflow_tasks = models.ManyToManyField(WorkflowTask)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="completed_user")
    completed_date = models.DateTimeField(null=True, blank=True)

    def create_workflow_tasks(self):
        tasks = self.activity.tasks.all()
        for task in tasks:
            workflow_task = WorkflowTask.objects.create(task=task, status="Not Started")
            self.workflow_tasks.add(workflow_task)
        self.save()

    def checkTasksStatuses(self):
        tasks = self.workflow_tasks.all()
        for t in tasks:
            # If any tasks are anything but complete, return False immediately and stop checking.
            if t.status != "Complete":
                return False
        return True

    def set_workflow_activity_active(self):
        self.status = "Active"
        self.save()
        # Schedule a job to email the new task notice.
        job = Job.objects.create(name="New Task Email")
        jco = JobCallable(self.email_users)
        job.job_code_object = jco
        job.run_every = timedelta(minutes=1)
        job.run_count_limit = 1
        job.delete_on_run_count_limit = True
        job.save()

    def start_tasks(self):
        workflow_tasks = self.workflow_tasks.all()
        for workflow_task in workflow_tasks:
            task = workflow_task.task
            if task.task_type == "Observer":
                args = {
                    "workflow_task": workflow_task,
                    "username": "tandem",
                    "status": True,
                }
                status, message = workflow_task.run_task(args)
                if not status:
                    workflow_task.start_observer(5, args)
                    workflow_task.status = "Running"
            else:
                workflow_task.status = "Waiting"
        workflow_task.save()

    def advance_workflow_activity(self, user=None):
        # Make sure all tasks are complete. If not, immediately stop.
        if not self.checkTasksStatuses():
            return False
        workflow = self.workflow
        self.status = "Complete"
        self.completed_date = datetime.now()
        if user is not None:
            self.completed_by = user
        self.save()
        children = self.activity.children.all()
        for activity in children:
            # Keeping some other ways to do this commented out. Will eventually delete these comments.
            # child_workflow_activity_set = WorkflowActivity.objects.filter(activity__pk__exact=activity.pk, workflow__pk__exact=workflow.pk)
            # child_workflow_activity_set = WorkflowActivity.objects.filter(activity=activity, workflow=workflow)
            child_workflow_activity_set = workflow.workflow_activites.filter(activity=activity)
            for child_workflow_activity in child_workflow_activity_set:
                child_workflow_activity.set_workflow_activity_active()
                child_workflow_activity.start_tasks()
        self.workflow.check_for_completeness()
        return True

    def email_users(self):
        if settings.EMAIL_ACTIVE:
            subject = "Tandem - Action required: " + self.activity.name
            for user in self.activity.users.all():
                body = "Hello, " + user.username + ". This is an automated e-mail from Tandem. You have a new task to complete: " + self.activity.name + ". For: " + self.workflow.person.first_name + " " + self.workflow.person.last_name
                send_mail(subject, body, settings.EMAIL_FROM_ADDRESS, [user.email], fail_silently=True)


class TaskWorker:

        # Proof of concept on a TaskWorker function. Needs to be cleaned up.
        def get_person_from_workflow_task(workflow_task):
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                return workflow_activity.workflow.person

        def get_employee_from_workflow_task(workflow_task):
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            return person.employee

        def get_person_workflow_from_workflow_task(workflow_task):
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                return workflow_activity.workflow.person.current_workflow

        def get_workflow_from_workflow_task(workflow_task):
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                return workflow_activity.workflow

        def is_epar_dup(epar_id):
            a = Employee.objects.filter(epar_id=epar_id)
            if a:
                return True
            return False

        def is_term_epar_dup(epar_id):
            a = Employee.objects.filter(termination_epar_id=epar_id)
            if a:
                return True
            return False

        def is_transfer_epar_dup(epar_id):
            a = Employee.objects.filter(transfer_epar_id=epar_id)
            if a:
                return True
            return False

        def is_visions_id_dup(visions_id):
            a = Employee.objects.filter(visions_id=visions_id)
            if a:
                return True
            return False

        def get_user_or_false(username):
            try:
                return User.objects.get(username=username)
            except ObjectDoesNotExist:
                return False

        def update_positions(employee, visions_positions):
            secondary_positions = []
            primary_position = employee.positions.get(is_primary=True)
            did_update = False
            for position in visions_positions:
                if position.position_ranking == "Primary":
                    location = VisionsHelper.get_position_location(position.dac)
                    primary_position.title = position.description
                    primary_position.visions_position_id = position.id
                    primary_position.last_updated_by = "Visions"
                    primary_position.last_updated_date = date.today()
                    if location:
                        primary_position.location = location
                    primary_position.save()
                    did_update = True
                else:
                    secondary_positions.append(position)
            if secondary_positions:
                for secondary_position in secondary_positions:
                    new_position = Position.objects.create(
                        person=employee,
                        title=secondary_position.description,
                        is_primary=False,
                        last_updated_by="Visions",
                        last_updated_date=date.today()
                    )
                    location = VisionsHelper.get_position_location(secondary_position.dac)
                    if location:
                        secondary_position.location = location
                        new_position.save()
                    did_update = True
            if did_update:
                return (True, "Success")
            return (False, "Nothing Updated")

        def task_update_name(**kwargs):
            workflow_activity = kwargs["workflow_activity"]
            first_name = kwargs["first_name"]
            last_name = kwargs["last_name"]
            person = workflow_activity.workflow.person
            person.first_name = first_name
            person.last_name = last_name
            person.save()
            return (True, "Success")

        def task_update_employee_id(**kwargs):
            return (True, "Success")

        def task_dummy(**kwargs):
            return (True, "Success")

        def task_set_epar_id(**kwargs):
            workflow_task = kwargs["workflow_task"]
            epar_id = kwargs["epar_id"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not VisionsHelper.verify_epar(epar_id):
                return (False, "ePAR not found")
            if TaskWorker.is_epar_dup(epar_id):
                return (False, "ePAR already linked to an Employee")
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            update_field(employee, "epar_id", epar_id, user)
            return (True, "Success")

        def task_set_term_epar_id(**kwargs):
            workflow_task = kwargs["workflow_task"]
            epar_id = kwargs["epar_id"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not VisionsHelper.verify_epar(epar_id):
                return (False, "ePAR not found")
            if TaskWorker.is_term_epar_dup(epar_id):
                return (False, "ePAR already linked to an Employee")
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            update_field(employee, "termination_epar_id", epar_id, user)
            return (True, "Success")

        def task_set_transfer_epar_id(**kwargs):
            workflow_task = kwargs["workflow_task"]
            epar_id = kwargs["epar_id"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not VisionsHelper.verify_epar(epar_id):
                return (False, "ePAR not found")
            if TaskWorker.is_transfer_epar_dup(epar_id):
                return (False, "ePAR already linked to an Employee")
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            update_field(employee, "transfer_epar_id", epar_id, user)
            positions = VisionsHelper.get_epar_positions(epar_id)
            if positions:
                return TaskWorker.update_positions(employee, positions)
            else:
                return (False, "No ePAR Positions Found")

        def task_assign_locations(**kwargs):
            workflow_task = kwargs["workflow_task"]
            locations = kwargs["locations"]
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            if not locations:
                return (False, "No locations")
            person.locations.clear()
            for location in locations:
                try:
                    new_location = Location.objects.get(id=location)
                except ObjectDoesNotExist:
                    return (False, "Invalid Location")
                person.locations.add(new_location)
            return (True, "Success")

        def task_set_visions_id(**kwargs):
            workflow_task = kwargs["workflow_task"]
            visions_id = kwargs["visions_id"]
            if not VisionsHelper.verify_employee(visions_id):
                return (False, "Employee not found")
            if TaskWorker.is_visions_id_dup(visions_id):
                return (False, "Visions Employee already linked to an Employee")
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            employee.visions_id = visions_id
            employee.save()
            employee.update_employee_from_visions()
            return (True, "Success")

        def task_check_ad(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            ad_username = ldap.get_ad_username_from_visions_id(employee.visions_id)
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if not ad_username:
                return (False, "Active Directory user not found")
            did_update = employee.update_ad_service(ad_username, user)
            if did_update:
                return (True, "Success")
            else:
                return (False, "Unknown Error")

        def task_disable_ad(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            ad_username = ldap.get_ad_username_from_visions_id(employee.visions_id)
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if ad_username:
                return (False, "Active Directory account still active")
            did_update = employee.disable_ad_service(user)
            if did_update:
                return (True, "Success")
            else:
                return (True, "No Active Directory account to disable.")

        def task_check_synergy(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            if "status" in kwargs:
                status = kwargs["status"]
                if not status:
                    update_field(employee, "is_synergy_account_needed", False)
                    return ("True", "Success")
            synergy_username = SynergyHelper.get_synergy_login(employee.visions_id)
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if not synergy_username:
                return (False, "Synergy user not found")
            did_update = employee.update_synergy_service(synergy_username, user)
            if did_update:
                return (True, "Success")
            else:
                return (False, "Unknown Error")

        def task_disable_synergy(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            synergy_username = SynergyHelper.get_synergy_login(employee.visions_id)
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if synergy_username:
                return (False, "Synergy user still active")
            did_update = employee.disable_synergy_service(user)
            if did_update:
                return (True, "Success")
            else:
                return (True, "No Synergy account to disable")

        def task_transfer_synergy(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            # If the 'status' arg is defined, that means the request
            # originated from the front end. We need to check it and
            # see if the user opted to skip over Synergy creation.
            if "status" in kwargs:
                status = kwargs["status"]
                if not status:
                    update_field(employee, "is_synergy_account_needed", False)
                    return ("True", "Success")
            synergy_username = SynergyHelper.get_synergy_login(employee.visions_id)
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if not synergy_username:
                return (True, "Success. The employee/contractor has no Synergy account.")
            did_update = employee.update_synergy_service(synergy_username, user)
            if did_update:
                return (True, "Success")
            else:
                return (False, "Unknown Error")

        def task_update_position(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            visions_positions = VisionsHelper.get_positions_for_employee(employee.visions_id)
            if not visions_positions:
                return (False, "No positions found")
            return TaskWorker.update_positions(employee, visions_positions)

        def task_set_tcp_id(**kwargs):
            workflow_task = kwargs["workflow_task"]
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            tcp_id = VisionsHelper.get_tcp_id_for_employee(employee.visions_id)
            if not tcp_id:
                return (False, "No Time Clock Plus record found in Visions")
            else:
                employee.tcp_id = tcp_id
                employee.save()
                return (True, "Success")

        def task_is_onboarded(**kwargs):
            workflow_task = kwargs["workflow_task"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            person.is_onboarded = True
            person.onboarded_by = user
            person.onboarded_date = datetime.now()
            person.save()
            return (True, "Success")

        def task_is_fingerprinted(**kwargs):
            workflow_task = kwargs["workflow_task"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            person.is_tcp_fingerprinted = True
            person.tcp_fingerprinted_by = user
            person.tcp_fingerprinted_date = datetime.now()
            person.save()
            return (True, "Success")

        def task_is_badge_created(**kwargs):
            workflow_task = kwargs["workflow_task"]
            user = TaskWorker.get_user_or_false(kwargs["username"])
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            person.is_badge_created = True
            person.badge_created_by = user
            person.badge_created_date = datetime.now()
            person.save()
            return (True, "Success")

        def task_cancel_workflow(**kwargs):
            workflow_task = kwargs["workflow_task"]
            cancel_workflow = TaskWorker.get_person_workflow_from_workflow_task(workflow_task)
            cancel_workflow.status = "Canceled"
            cancel_workflow.cancel_all_jobs()
            cancel_workflow.save()
            workflow = TaskWorker.get_workflow_from_workflow_task(workflow_task)
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            person.current_workflow = workflow
            person.cancel_workflow = cancel_workflow
            person.save()
            return (True, "Success")

        def task_reverse_ad(**kwargs):
            return (True, "Success")

        def task_reverse_synergy(**kwargs):
            return (True, "Success")

        def task_reverse_visions(**kwargs):
            return (True, "Success")

        def task_mark_long_term(**kwargs):
            workflow_task = kwargs["workflow_task"]
            visions_id = kwargs["visions_id"]
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            if visions_id and visions_id != "":
                if not VisionsHelper.verify_employee(visions_id):
                    return (False, "Employee not found")
                else:
                    person.long_term_sub_replacing = visions_id
            person.long_term_sub = True
            person.save()
            return (True, "Success")

        def task_create_long_term_synergy(**kwargs):
            workflow_task = kwargs["workflow_task"]
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            # If the 'status' arg is defined, that means the request
            # originated from the front end. We need to check it and
            # see if the user opted to skip over Synergy creation.
            if "status" in kwargs:
                status = kwargs["status"]
                if not status:
                    update_field(person, "is_synergy_account_needed", False)
                    return ("True", "Success")
            if kwargs["synergy_username"] == "":
                return ("False", "No Synergy username entered.")
            synergy_username = SynergyHelper.verify_synergy_username(kwargs["synergy_username"])
            user = TaskWorker.get_user_or_false(kwargs["username"])
            if not user:
                return (False, "Invalid User")
            if not synergy_username:
                return (False, "Synergy user not found")
            did_update = person.update_synergy_service(synergy_username, user)
            if did_update:
                return (True, "Success")
            else:
                return (False, "Unknown Error")

        def task_create_long_term_ad(**kwargs):
            workflow_task = kwargs["workflow_task"]
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            if kwargs["ad_username"] == "":
                return ("False", "No Active Directory username entered.")
            user = TaskWorker.get_user_or_false(kwargs["username"])
            ad_username = kwargs["ad_username"]
            if not user:
                return (False, "Invalid User")
            if not ldap.is_ad_username_active(ad_username):
                return (False, "Active Directory user not found")
            did_update = person.update_ad_service(ad_username, user)
            if did_update:
                return (True, "Success")
            else:
                return (False, "Unknown Error")
