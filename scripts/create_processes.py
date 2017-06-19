from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity
from django.contrib.auth.models import User


def run():
    # Delete everything
    Process.objects.all().delete()
    Activity.objects.all().delete()
    Task.objects.all().delete()
    Workflow.objects.all().delete()
    WorkflowActivity.objects.all().delete()

    # TEMP: Get tharris user to add to everything
    tharris = User.objects.get(username="tharris")

    # Create Processes
    new_hire_process = Process.objects.create(name="New Hire Process")
    new_hire_process.save()

    # Create Tasks
    # Step 1
    create_epar_task = Task.objects.create(name="Create ePAR", task_function="task_set_epar_id", task_type="Observer")
    create_epar_task.save()

    # Step 2
    create_visions_record_task = Task.objects.create(name="Create Employee Maintenance Record", task_function="task_set_visions_id", task_type="Observer")
    create_visions_record_task.save()

    # Step 3
    assign_to_position_task = Task.objects.create(name="Assign Employee to Visions Position", task_function="task_update_position", task_type="Observer")
    assign_to_position_task.save()

    create_ad_account_task = Task.objects.create(name="Create Active Directory Account", task_function="task_check_ad", task_type="Observer")
    create_ad_account_task.save()

    create_synergy_account_task = Task.objects.create(name="Create Synergy Account", task_function="task_check_synergy", task_type="Observer")
    create_synergy_account_task.save()

    # Step 4
    create_tcp_account_task = Task.objects.create(name="Create TCP Account", task_function="task_set_tcp_id", task_type="User")
    create_tcp_account_task.save()

    # Step 5
    onboard_employee_task = Task.objects.create(name="Onboard Employee", task_function="task_is_onboarded", task_type="User")
    onboard_employee_task.save()

    # Step 6
    tcp_fingerprint_employee_task = Task.objects.create(name="TCP Fingerprint Employee", task_function="task_is_fingerprinted", task_type="User")
    tcp_fingerprint_employee_task.save()

    # Step 7
    badge_created_task = Task.objects.create(name="Employee Badge Printed", task_function="task_is_badge_created", task_type="User")
    badge_created_task.save()

    # Create Activities
    # Step 7
    badge_created_activity = Activity.objects.create(name="Employee Badge Printed", process=new_hire_process)
    badge_created_activity.tasks.add(badge_created_task)
    badge_created_activity.users.add(tharris)
    badge_created_activity.save()

    # Step 6
    tcp_fingerprint_employee_activity = Activity.objects.create(name="TCP Fingerprint Employee", process=new_hire_process)
    tcp_fingerprint_employee_activity.tasks.add(tcp_fingerprint_employee_task)
    tcp_fingerprint_employee_activity.users.add(tharris)
    tcp_fingerprint_employee_activity.children.add(badge_created_activity)
    tcp_fingerprint_employee_activity.save()

    # Step 5
    onboard_employee_activity = Activity.objects.create(name="Onboard Employee", process=new_hire_process)
    onboard_employee_activity.tasks.add(onboard_employee_task)
    onboard_employee_activity.users.add(tharris)
    onboard_employee_activity.children.add(tcp_fingerprint_employee_activity)
    onboard_employee_activity.save()

    # Step 4
    create_tcp_account_activity = Activity.objects.create(name="Create TCP Account", process=new_hire_process)
    create_tcp_account_activity.tasks.add(create_tcp_account_task)
    create_tcp_account_activity.users.add(tharris)
    create_tcp_account_activity.children.add(onboard_employee_activity)
    create_tcp_account_activity.save()

    # Step 3
    assign_to_position_activity = Activity.objects.create(name="Assign Employee to Visions Position", process=new_hire_process)
    assign_to_position_activity.tasks.add(assign_to_position_task)
    assign_to_position_activity.users.add(tharris)
    assign_to_position_activity.children.add(create_tcp_account_activity)
    assign_to_position_activity.save()

    create_ad_account_activity = Activity.objects.create(name="Create Active Directory Account", process=new_hire_process)
    create_ad_account_activity.tasks.add(create_ad_account_task)
    create_ad_account_activity.users.add(tharris)
    create_ad_account_activity.save()

    create_synergy_account_activity = Activity.objects.create(name="Create Synergy Account", process=new_hire_process)
    create_synergy_account_activity.tasks.add(create_synergy_account_task)
    create_synergy_account_activity.users.add(tharris)
    create_synergy_account_activity.save()

    # Step 2
    create_visions_record_activity = Activity.objects.create(name="Create Employee Maintenance Record", process=new_hire_process)
    create_visions_record_activity.tasks.add(create_visions_record_task)
    create_visions_record_activity.users.add(tharris)
    create_visions_record_activity.children.add(assign_to_position_activity)
    create_visions_record_activity.children.add(create_ad_account_activity)
    create_visions_record_activity.children.add(create_synergy_account_activity)
    create_visions_record_activity.save()

    # Step 1
    create_epar_activity = Activity.objects.create(name="Create ePAR", process=new_hire_process)
    create_epar_activity.tasks.add(create_epar_task)
    create_epar_activity.users.add(tharris)
    create_epar_activity.children.add(create_visions_record_activity)
    create_epar_activity.save()

    # Add Start Activities to Processes
    new_hire_process.start_activity = create_epar_activity
    new_hire_process.save()
