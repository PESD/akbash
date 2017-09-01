from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity
from django.contrib.auth.models import User


def run():
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

    new_hire_process = Process.objects.get(name="New Hire Process")

    assign_locations_task = Task.objects.get(name="Assign Work Locations")

    create_visions_record_activity = Activity.objects.get(name="Create Employee Maintenance Record")

    update_locations_activity = Activity.objects.create(name="Assign Work Locations", process=new_hire_process)
    update_locations_activity.tasks.add(assign_locations_task)
    update_locations_activity.users.add(tharris)
    update_locations_activity.users.add(lauren)
    update_locations_activity.users.add(mario)
    update_locations_activity.users.add(claudia)
    update_locations_activity.users.add(pat)
    update_locations_activity.children.add(create_visions_record_activity)
    update_locations_activity.save()

    create_epar_activity = Activity.objects.get(name="Create ePAR")
    create_epar_activity.children.clear()
    create_epar_activity.children.add(update_locations_activity)
    create_epar_activity.save()
