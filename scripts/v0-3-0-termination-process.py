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
    termination_process = Process.objects.create(name="Termination Process")

    # Termination Tasks
    # Step 1 - Termination ePAR
    create_term_epar_task = Task.objects.create(name="Create Termination ePAR", task_function="task_set_term_epar_id", task_type="Observer")
    # Step 2.1 - Disable Active Directory
    disable_ad_account_task = Task.objects.create(name="Disable Active Directory Account", task_function="task_disable_ad", task_type="Observer")
    # Step 2.2 - Disable Synergy
    disable_synergy_account_task = Task.objects.create(name="Disable Synergy Account", task_function="task_disable_synergy", task_type="Observer")

    # Termination Activities
    # Step 2 - Disable Synergy & AD
    disable_synergy_account_activity = Activity.objects.create(name="Disable Synergy Account", process=termination_process)
    disable_synergy_account_activity.tasks.add(disable_synergy_account_task)
    disable_synergy_account_activity.users.add(marie)
    disable_synergy_account_activity.users.add(paul)
    disable_synergy_account_activity.users.add(tharris)
    disable_synergy_account_activity.save()

    disable_ad_account_activity = Activity.objects.create(name="Disable Active Directory Account", process=termination_process)
    disable_ad_account_activity.tasks.add(disable_ad_account_task)
    disable_ad_account_activity.users.add(tharris)
    disable_ad_account_activity.users.add(rocky)
    disable_ad_account_activity.users.add(larhea)
    disable_ad_account_activity.users.add(david)
    disable_ad_account_activity.save()

    # Step 1 - Create Termination ePAR
    create_term_epar_activity = Activity.objects.create(name="Create Termination ePAR", process=termination_process)
    create_term_epar_activity.tasks.add(create_term_epar_task)
    create_term_epar_activity.users.add(tharris)
    create_term_epar_activity.users.add(lauren)
    create_term_epar_activity.users.add(mario)
    create_term_epar_activity.users.add(claudia)
    create_term_epar_activity.users.add(pat)
    create_term_epar_activity.children.add(disable_ad_account_activity)
    create_term_epar_activity.children.add(disable_synergy_account_activity)
    create_term_epar_activity.save()

    # Add Start Activity to Termination Process
    termination_process.start_activity = create_term_epar_activity
    termination_process.save()
