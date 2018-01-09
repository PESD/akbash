from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity, ProcessCategory
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

    # Activate Long-term Sub Process
    existing_employee_cat = ProcessCategory.objects.get(name="Existing Employee")
    deactivate_sub_process = Process.objects.create(name="Deactivate Long-term Sub Process")
    deactivate_sub_process.categories.add(existing_employee_cat)
    deactivate_sub_process.save()

    # Activate Long-term Sub Tasks
    # Step 1 - Mark as Long-term Sub
    remove_long_term_task = Task.objects.create(name="Remove as Long-term Sub", task_function="task_remove_long_term", task_type="Observer")
    # Step 2.1 - Create Long Term Sub Active Directory Account
    deactivate_long_term_ad_task = Task.objects.create(name="Disable Long-term Sub Active Directory Account", task_function="task_deactivate_long_term_ad", task_type="User")
    # Step 2.2 - Create Long Term Sub Synergy Account
    deactivate_long_term_synergy_task = Task.objects.create(name="Disable Long-term Sub Synergy Account", task_function="task_deactivate_long_term_synergy", task_type="User")

    # Activate Long-term Sub Activities
    # Step 2 - Create Synergy & AD
    deactivate_long_term_synergy_activity = Activity.objects.create(name="Disable Long-term Sub Synergy Account", process=deactivate_sub_process)
    deactivate_long_term_synergy_activity.tasks.add(deactivate_long_term_synergy_task)
    deactivate_long_term_synergy_activity.users.add(marie)
    deactivate_long_term_synergy_activity.users.add(paul)
    deactivate_long_term_synergy_activity.users.add(tharris)
    deactivate_long_term_synergy_activity.save()

    deactivate_long_term_ad_activity = Activity.objects.create(name="Disable Long-term Sub Active Directory Account", process=deactivate_sub_process)
    deactivate_long_term_ad_activity.tasks.add(deactivate_long_term_ad_task)
    deactivate_long_term_ad_activity.users.add(tharris)
    deactivate_long_term_ad_activity.users.add(rocky)
    deactivate_long_term_ad_activity.users.add(larhea)
    deactivate_long_term_ad_activity.users.add(david)
    deactivate_long_term_ad_activity.save()

    # Step 1 - Mark as Long Term Sub task
    remove_long_term_activity = Activity.objects.create(name="Remove as Long-term Sub", process=deactivate_sub_process)
    remove_long_term_activity.tasks.add(remove_long_term_task)
    remove_long_term_activity.users.add(tharris)
    remove_long_term_activity.children.add(deactivate_long_term_ad_activity)
    remove_long_term_activity.children.add(deactivate_long_term_synergy_activity)
    remove_long_term_activity.save()

    # Add Start Activity to Activate Long-term Sub Process
    deactivate_sub_process.start_activity = remove_long_term_activity
    deactivate_sub_process.save()
