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

    # Create transfer process
    transfer_process = Process.objects.create(name="Transfer Process")

    # Transefer Tasks
    # Step 1 - Transfer ePAR
    create_transfer_epar_task = Task.objects.create(name="Create Transfer ePAR", task_function="task_set_transfer_epar_id", task_type="Observer")
    # Step 2 - Assign Locations
    assign_locations_task = Task.objects.create(name="Assign Work Locations", task_function="task_assign_locations", task_type="User")
    # Step 3.1 - Assign to Visions Position(s)
    assign_to_position_task = Task.objects.get(name="Assign Employee to Visions Position")
    # Step 3.2 - Change Active Directory
    transfer_ad_account_task = Task.objects.get(name="Create Active Directory Account")
    # Step 3.3 - Change Synergy
    transfer_synergy_account_task = Task.objects.create(name="Transfer Synergy Account", task_function="task_transfer_synergy", task_type="Observer")

    # Transfer Activities
    # Step 3 - Transfer Synergy & AD
    transfer_synergy_account_activity = Activity.objects.create(name="Transfer Synergy Account", process=transfer_process)
    transfer_synergy_account_activity.tasks.add(transfer_synergy_account_task)
    transfer_synergy_account_activity.users.add(marie)
    transfer_synergy_account_activity.users.add(paul)
    transfer_synergy_account_activity.users.add(tharris)
    transfer_synergy_account_activity.save()

    transfer_ad_account_activity = Activity.objects.create(name="Transfer Active Directory Account", process=transfer_process)
    transfer_ad_account_activity.tasks.add(transfer_ad_account_task)
    transfer_ad_account_activity.users.add(tharris)
    transfer_ad_account_activity.users.add(rocky)
    transfer_ad_account_activity.users.add(larhea)
    transfer_ad_account_activity.users.add(david)
    transfer_ad_account_activity.save()

    assign_to_position_activity = Activity.objects.create(name="Assign Employee to Visions Position", process=transfer_process)
    assign_to_position_activity.tasks.add(assign_to_position_task)
    assign_to_position_activity.users.add(tharris)
    assign_to_position_activity.users.add(matthew)
    assign_to_position_activity.users.add(frank)
    assign_to_position_activity.save()

    # Step 2 - Assign Locations
    assign_locations_activity = Activity.objects.create(name="Assign Locations", process=transfer_process)
    assign_locations_activity.tasks.add(assign_locations_task)
    assign_locations_activity.users.add(tharris)
    assign_locations_activity.users.add(lauren)
    assign_locations_activity.users.add(mario)
    assign_locations_activity.users.add(claudia)
    assign_locations_activity.users.add(pat)
    assign_locations_activity.children.add(transfer_ad_account_activity)
    assign_locations_activity.children.add(transfer_synergy_account_activity)
    assign_locations_activity.children.add(assign_to_position_activity)
    assign_locations_activity.save()

    # Step 1 - Create Transfer ePAR
    create_transfer_epar_activity = Activity.objects.create(name="Create Transfer ePAR", process=transfer_process)
    create_transfer_epar_activity.tasks.add(create_transfer_epar_task)
    create_transfer_epar_activity.users.add(tharris)
    create_transfer_epar_activity.users.add(lauren)
    create_transfer_epar_activity.users.add(mario)
    create_transfer_epar_activity.users.add(claudia)
    create_transfer_epar_activity.users.add(pat)
    create_transfer_epar_activity.children.add(assign_locations_activity)
    create_transfer_epar_activity.save()

    # Add Start Activity to Termination Process
    transfer_process.start_activity = create_transfer_epar_activity
    transfer_process.save()
