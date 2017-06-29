from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from api.models import Person, Employee
from django.contrib.auth.models import User
from bpm.visions_helper import VisionsHelper


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


class Process(models.Model):
    name = models.CharField(max_length=255)
    start_activity = models.ForeignKey(
        "Activity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    def start_workflow(self, person):
        workflow = Workflow.objects.create(person=person, process=self)
        workflow.save()
        person.generate_badge()
        activities = self.activities.all()
        for activity in activities:
            workflow_activity = workflow.create_workflow_activity(activity)
            if activity == self.start_activity:
                workflow_activity.set_workflow_activity_active()
        return workflow


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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)

    def get_current_workflow_activities(self):
        return self.workflow_activites.filter(status="Active")

    def create_workflow_activity(self, activity):
        workflow_activity = WorkflowActivity.objects.create(workflow=self, activity=activity, status="Inactive")
        workflow_activity.save()
        workflow_activity.create_workflow_tasks()
        return workflow_activity


class WorkflowTask(models.Model):
    STATUSES = (
        ("Not Started", "Not Started"),
        ("Running", "Running"),
        ("Waiting", "Waiting"),
        ("Error", "Error"),
        ("Complete", "Complete")
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUSES)

    def run_task(self, args):
        status, message = self.task.task_controller_function(args)
        self.status = "Complete" if status else "Error"
        self.save()
        return (status, message)


class WorkflowActivity(models.Model):
    STATUSES = (
        ("Complete", "Complete"),
        ("Error", "Error"),
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Next", "Next")
    )
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="workflow_activites")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUSES)
    workflow_tasks = models.ManyToManyField(WorkflowTask)

    def create_workflow_tasks(self):
        tasks = self.activity.tasks.all()
        for task in tasks:
            workflow_task = WorkflowTask.objects.create(task=task, status="Not Started")
            task.save()
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
        self.email_users()

    def advance_workflow_activity(self):
        # Make sure all tasks are complete. If not, immediately stop.
        if not self.checkTasksStatuses():
            return False
        workflow = self.workflow
        self.status = "Complete"
        self.save()
        children = self.activity.children.all()
        for activity in children:
            # Keeping some other ways to do this commented out. Will eventually delete these comments.
            # child_workflow_activity_set = WorkflowActivity.objects.filter(activity__pk__exact=activity.pk, workflow__pk__exact=workflow.pk)
            # child_workflow_activity_set = WorkflowActivity.objects.filter(activity=activity, workflow=workflow)
            child_workflow_activity_set = workflow.workflow_activites.filter(activity=activity)
            for child_workflow_activity in child_workflow_activity_set:
                child_workflow_activity.set_workflow_activity_active()
        return True

    def email_users(self):
        subject = "Action required: " + self.activity.name
        for user in self.activity.users.all():
            body = "Hello, " + user.username + " you have a new task to complete."
            send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


class TaskWorker:

        # Proof of concept on a TaskWorker function. Needs to be cleaned up.
        def get_person_from_workflow_task(workflow_task):
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                return workflow_activity.workflow.person

        def get_employee_from_workflow_task(workflow_task):
            person = TaskWorker.get_person_from_workflow_task(workflow_task)
            return person.employee

        def is_epar_dup(epar_id):
            a = Employee.objects.filter(epar_id=epar_id)
            if a:
                return True
            return False

        def is_visions_id_dup(visions_id):
            a = Employee.objects.filter(visions_id=visions_id)
            if a:
                return True
            return False

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
            if not VisionsHelper.verify_epar(epar_id):
                return (False, "ePAR not found")
            if TaskWorker.is_epar_dup(epar_id):
                return (False, "ePAR already linked to an Employee")
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            employee.epar_id = epar_id
            employee.save()
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
            return (True, "Success")
