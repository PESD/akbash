from django.db import models
from api.models import Person


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


class Task(models.Model):
    name = models.CharField(max_length=255)
    task_function = models.CharField(max_length=255)

    def task_controller_function(self, args):
        return getattr(TaskWorker, self.task_function)(**args)


class Activity(models.Model):
    name = models.CharField(max_length=255)
    children = models.ManyToManyField("Activity")
    tasks = models.ManyToManyField(Task)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)


class Workflow(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)


class WorkflowActivity(models.Model):
    STATUSES = (
        ("Complete", "Complete"),
        ("Error", "Error"),
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Next", "Next")
    )
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUSES)


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
