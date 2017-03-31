from django.test import TestCase
from api.models import Person, Employee
from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity
from bpm.task_controller import TaskWorker

# Create your tests here.


class WorkflowTestCase(TestCase):
    def setUp(self):
        new_hire = Process.objects.create(name="New Hire Process")
        new_hire.save()
        update_name_task = Task.objects.create(name="Update Name", task_function="task_update_name")
        update_name_task.save()
        update_name_activity = Activity.objects.create(name="Update Name", process=new_hire)
        update_name_activity.tasks.add(update_name_task)
        update_name_activity.save()
        ned = Employee.objects.create(first_name="Ned", last_name="Stark")
        ned.talented_id = 11111
        ned.save()
        ned_workflow = Workflow.objects.create(person=ned, process=new_hire)
        ned_workflow.save()
        ned_update_name = WorkflowActivity(
            workflow=ned_workflow,
            activity=update_name_activity,
            status="Active",
        )
        ned_update_name.save()

    def test_name_change(self):
        ned = Employee.objects.get(talented_id=11111)
        workflow = Workflow.objects.get(person=ned)
        workflow_activity = WorkflowActivity.objects.get(workflow=workflow, status="Active")
        activity = workflow_activity.activity
        tasks = activity.tasks.all()
        i = 0
        for t in tasks:
            args = {
                "workflow_activity": workflow_activity,
                "first_name": "Eddard",
                "last_name": "Starky",
            }
            tw = t.task_controller_function(args)
            i = i + 1
        new_ned = Employee.objects.get(talented_id=11111)
        self.assertEqual(i, 1)
        self.assertEqual(new_ned.first_name, "Eddard")
