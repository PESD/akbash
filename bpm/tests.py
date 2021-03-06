from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Person, Employee
from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity, TaskWorker, WorkflowTask

# Create your tests here.


class WorkflowTestCase(TestCase):
    def setUp(self):
        # Create some users to assign to Activities
        user = User.objects.create_user('jsnow', 'jsnow@winterfell.com', 'ghost')
        user.last_name = "Snow"
        user.save()
        user2 = User.objects.create_user('astark', 'astark@winterfell.com', 'nymeria')
        user2.last_name = "Stark"
        user2.save()
        # Create some BPM objects and an Employee for our tests.
        # Start with creating a New Hire Process
        new_hire = Process.objects.create(name="New Hire Process")
        new_hire.save()
        # Create some tasks
        update_name_task = Task.objects.create(name="Update Name", task_function="task_update_name", task_type="User")
        update_name_task.save()
        update_employee_id_task = Task.objects.create(name="Update Employee ID", task_function="task_update_employee_id", task_type="Observer")
        update_employee_id_task.save()
        # Create some activities
        update_name_activity = Activity.objects.create(name="Update Name", process=new_hire)
        update_name_activity.tasks.add(update_name_task)
        update_name_activity.users.add(user)
        update_name_activity.save()
        update_employee_id_activity = Activity.objects.create(name="Update Employee ID", process=new_hire)
        update_employee_id_activity.tasks.add(update_employee_id_task)
        update_employee_id_activity.users.add(user2)
        update_employee_id_activity.save()
        # Give update name activity a child activity of update employee ID
        update_name_activity.children.add(update_employee_id_activity)
        update_name_activity.save()
        # Set the starting activity for the New Hire Process
        new_hire.start_activity = update_name_activity
        new_hire.save()
        # Create an employee
        ned = Employee.objects.create(first_name="Ned", last_name="Stark")
        ned.talented_id = 11111
        ned.save()
        # Create a new Workflow based on New Hire Process and the Ned Stark employee we created
        workflow = new_hire.start_workflow(ned)

    def test_workflow(self):
        ned = Employee.objects.get(talented_id=11111)
        workflow = Workflow.objects.get(person=ned)
        current_activity = workflow.get_current_workflow_activities()[0]
        tasks = current_activity.workflow_tasks.all()
        i = 0
        for task in tasks:
            args = {}
            if task.task.name == 'Update Name':
                args = {
                    "workflow_activity": current_activity,
                    "first_name": "Eddard",
                    "last_name": "Starky",
                }
            status, message = task.run_task(args)
            self.assertIs(status, True)
            self.assertEqual("Success", message)
            i = i + 1
        # Does the number of tasks equal what we think it should?
        self.assertEqual(i, 1)
        # Make sure that Ned's first name was changed to Eddard
        new_ned = Employee.objects.get(talented_id=11111)
        self.assertEqual(new_ned.first_name, "Eddard")
        # Make sure Jon Snow is the assigned user
        is_users_jon = False
        activity = current_activity.activity
        users = activity.users.all()
        for u in users:
            if u.username == "jsnow":
                is_users_jon = True
        self.assertIs(is_users_jon, True)
        current_activity.advance_workflow_activity()
        new_current_activities = workflow.get_current_workflow_activities()
        for new_current_activity in new_current_activities:
            self.assertEqual("Update Employee ID", new_current_activity.activity.name)
        self.assertNotEqual(None, ned.badge_number)
