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
    crystal = User.objects.get(username='crystal.senesy')
    pat = User.objects.get(username='pat.rogel')
    # Finance
    janice = User.objects.get(username='janice.durham')
    frank = User.objects.get(username='frank.kraatz')
    matthew = User.objects.get(username='matthew.cavazos')
    rosanna = User.objects.get(username='rosanna.hidalgo')

    # Activate Long-term Sub Process
    existing_employee_cat = ProcessCategory.objects.get(name="Existing Employee")
    activate_sub_process = Process.objects.create(name="Activate Long-term Sub Process")
    activate_sub_process.categories.add(existing_employee_cat)
    activate_sub_process.save()

    # Activate Long-term Sub Tasks
    # Step 1 - Mark as Long-term Sub
    mark_long_term_task = Task.objects.create(name="Mark as Long-term Sub", task_function="task_mark_long_term", task_type="User")
    # Step 2 - Assign Work Locations (use existing)
    assign_locations_task = Task.objects.get(name="Assign Work Locations")
    # Step 3.1 - Create Long Term Sub Active Directory Account
    create_long_term_ad_task = Task.objects.create(name="Create Long-term Sub Active Directory Account", task_function="task_create_long_term_ad", task_type="User")
    # Step 3.2 - Create Long Term Sub Synergy Account
    create_long_term_synergy_task = Task.objects.create(name="Create Long-term Sub Synergy Account", task_function="task_create_long_term_synergy", task_type="User")

    # Activate Long-term Sub Activities
    # Step 3 - Create Synergy & AD
    create_long_term_synergy_activity = Activity.objects.create(name="Create Long-term Sub Synergy Account", process=activate_sub_process)
    create_long_term_synergy_activity.tasks.add(create_long_term_synergy_task)
    create_long_term_synergy_activity.users.add(marie)
    create_long_term_synergy_activity.users.add(paul)
    create_long_term_synergy_activity.users.add(tharris)
    create_long_term_synergy_activity.save()

    create_long_term_ad_activity = Activity.objects.create(name="Create Long-term Sub Active Directory Account", process=activate_sub_process)
    create_long_term_ad_activity.tasks.add(create_long_term_ad_task)
    create_long_term_ad_activity.users.add(tharris)
    create_long_term_ad_activity.users.add(rocky)
    create_long_term_ad_activity.users.add(larhea)
    create_long_term_ad_activity.users.add(david)
    create_long_term_ad_activity.save()

    # Step 2 - Long Term Location task
    locations_long_term_activity = Activity.objects.create(name="Assign Long-term Sub Work Location", process=activate_sub_process)
    locations_long_term_activity.tasks.add(assign_locations_task)
    locations_long_term_activity.users.add(tharris)
    locations_long_term_activity.users.add(lauren)
    locations_long_term_activity.users.add(crystal)
    locations_long_term_activity.users.add(mario)
    locations_long_term_activity.users.add(pat)
    locations_long_term_activity.children.add(create_long_term_ad_activity)
    locations_long_term_activity.children.add(create_long_term_synergy_activity)
    locations_long_term_activity.save()

    # Step 1 - Mark as Long Term Sub task
    mark_long_term_activity = Activity.objects.create(name="Mark as Long-term Sub", process=activate_sub_process)
    mark_long_term_activity.tasks.add(mark_long_term_task)
    mark_long_term_activity.users.add(tharris)
    mark_long_term_activity.users.add(lauren)
    mark_long_term_activity.users.add(crystal)
    mark_long_term_activity.users.add(mario)
    mark_long_term_activity.users.add(pat)
    mark_long_term_activity.children.add(locations_long_term_activity)
    mark_long_term_activity.save()

    # Add Start Activity to Activate Long-term Sub Process
    activate_sub_process.start_activity = mark_long_term_activity
    activate_sub_process.save()
