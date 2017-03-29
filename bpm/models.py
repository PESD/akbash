from django.db import models
from api.models import Person
from bpm.task_controller import TaskWorker

# Create your models here.


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
