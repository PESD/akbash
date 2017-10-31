from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity
from django.contrib.auth.models import User


def run():
    # Get task workers
    # TEMP: Get tharris user to add to everything
    tharris = User.objects.get(username="tharris")
    # MIS
    marie = User.objects.get(username='mariev.clark')
    rocky = User.objects.get(username='rocky.berumen')
    larhea = User.objects.get(username='larheat.russell')
    david = User.objects.get(username='david.johnson')
    paul = User.objects.get(username='paul.chase')
    # HR
    lauren = User.objects.get(username='lauren.pagnotta')
    brandon = User.objects.get(username='brandon.soto')
    mario = User.objects.get(username='mario.romero')
    claudia = User.objects.get(username='claudia.fisher')
    pat = User.objects.get(username='pat.rogel')
    # Finance
    janice = User.objects.get(username='janice.durham')
    frank = User.objects.get(username='frank.kraatz')
    matthew = User.objects.get(username='matthew.cavazos')
    rosanna = User.objects.get(username='rosanna.hidalgo')

    # Termination Process
    cancel_workflow_process = Process.objects.create(name="Cancel Workflow Process")

    # Termination Tasks
    # Step 1 - Cancel Workflow
    cancel_workflow_task = Task.objects.create(name="Cancel Workflow", task_function="task_cancel_workflow", task_type="Observer")
    # Step 2.1 - Reverse Active Directory
    reverse_ad_task = Task.objects.create(name="Verify Possible Active Directory Account Reversion", task_function="task_reverse_ad", task_type="User")
    # Step 2.2 - Reverse Synergy
    reverse_synergy_account_task = Task.objects.create(name="Verify Possible Synergy Account Reversion", task_function="task_reverse_synergy", task_type="User")
    # Step 2.3 - Reverse Visions Positions
    reverse_visions_position_task = Task.objects.create(name="Verify Possible Visions Position Reversion", task_function="task_reverse_visions", task_type="User")

    # Termination Activities
    # Step 2 - Disable Synergy & AD
    reverse_synergy_account_activity = Activity.objects.create(name="Disable Synergy Account", process=termination_process)
    reverse_synergy_account_activity.tasks.add(reverse_synergy_account_task)
    reverse_synergy_account_activity.users.add(marie)
    reverse_synergy_account_activity.users.add(paul)
    reverse_synergy_account_activity.users.add(tharris)
    reverse_synergy_account_activity.save()

    reverse_ad_account_activity = Activity.objects.create(name="Disable Active Directory Account", process=termination_process)
    reverse_ad_account_activity.tasks.add(reverse_ad_account_task)
    reverse_ad_account_activity.users.add(tharris)
    reverse_ad_account_activity.users.add(rocky)
    reverse_ad_account_activity.users.add(larhea)
    reverse_ad_account_activity.users.add(david)
    reverse_ad_account_activity.save()

    reverse_visions_activity = Activity.objects.create(name="Disable Active Directory Account", process=termination_process)
    reverse_visions_activity.tasks.add(reverse_ad_account_task)
    reverse_visions_activity.users.add(tharris)
    reverse_visions_activity.users.add(matthew)
    reverse_visions_activity.users.add(frank)
    reverse_visions_activity.save()

    # Step 1 - Create Termination ePAR
    cancel_workflow_activity = Activity.objects.create(name="Cancel Workflow", process=cancel_workflow_process)
    cancel_workflow_activity.tasks.add(cancel_workflow_task)
    cancel_workflow_activity.users.add(tharris)
    cancel_workflow_activity.children.add(reverse_ad_account_activity)
    cancel_workflow_activity.children.add(reverse_synergy_account_activity)
    cancel_workflow_activity.children.add(reverse_visions_activity)
    cancel_workflow_activity.save()

    # Add Start Activity to Termination Process
    cancel_workflow_process.start_activity = cancel_workflow_activity
    cancel_workflow_process.save()
