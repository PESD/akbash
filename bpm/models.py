from django.db import models
from api.models import Person
from django.contrib.auth.models import User

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
        activities = self.activities.all()
        for activity in activities:
            workflow_activity = workflow.create_workflow_activity(activity)
            if activity == self.start_activity:
                workflow_activity.set_workflow_activity_active()
        return workflow


class Task(models.Model):
    name = models.CharField(max_length=255)
    task_function = models.CharField(max_length=255)

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
        return workflow_activity


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

    def set_workflow_activity_active(self):
        self.status = "Active"
        self.save()

    def advance_workflow_activity(self):
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
                child_workflow_activity.status = "Active"
                child_workflow_activity.save()


class TaskWorker:

        # Proof of concept on a TaskWorker function. Needs to be cleaned up.
        def task_update_name(**kwargs):
            workflow_activity = kwargs["workflow_activity"]
            first_name = kwargs["first_name"]
            last_name = kwargs["last_name"]
            person = workflow_activity.workflow.person
            person.first_name = first_name
            person.last_name = last_name
            person.save()

        def task_update_employee_id(**kwargs):
            pass
