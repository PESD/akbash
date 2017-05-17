from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Person, Employee
from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity, TaskWorker

# Create your tests here.


class WorkflowTestCase(TestCase):
    def setUp(self):
        # Create some BPM objects and an Employee for our tests.
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
        user = User.objects.create_user('jsnow', 'jsnow@winterfell.com', 'ghost')
        user.last_name = "Snow"
        user.save()
        user2 = User.objects.create_user('astark', 'astark@winterfell.com', 'nymeria')
        user2.last_name = "Stark"
        user2.save()
        update_name_activity.users.add(user)
        update_name_activity.users.add(user2)
        update_name_activity.save()

    def test_name_change(self):
        # Can we check the current WorkflowActivity's Activity's tasks and run those?
        # Ned Stark should change to Eddard Starky
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
        # Make sure that 1 task was returned.
        self.assertEqual(i, 1)
        # Make sure that Ned's first name changed to Eddard.
        self.assertEqual(new_ned.first_name, "Eddard")
        is_users_jon = False
        is_users_arya = False
        users = activity.users.all()
        for u in users:
            if u.username == "jsnow":
                is_users_jon = True
            elif u.username == "astark":
                is_users_arya = True
        self.assertIs(is_users_jon, True)
        self.assertIs(is_users_arya, True)
