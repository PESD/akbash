from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity
from api.models import Person, Employee, Contractor, Location, Position, PositionType, Vendor, VendorType
from django.contrib.auth.models import User
from api.xml_parse import parse_hires
from bpm.xml_request import get_talented_xml


def run():
    # Delete everything
    Process.objects.all().delete()
    Activity.objects.all().delete()
    Task.objects.all().delete()
    Workflow.objects.all().delete()
    WorkflowActivity.objects.all().delete()
    Position.objects.all().delete()
    Employee.objects.all().delete()
    Contractor.objects.all().delete()
    PositionType.objects.all().delete()
    Location.objects.all().delete()
    Vendor.objects.all().delete()
    VendorType.objects.all().delete()
    Person.objects.all().delete()

    # Locations
    locations = [
        {"name": "Bethune", "short_name": "Bethune", "number": "101"},
        {"name": "Capitol", "short_name": "Capitol", "number": "102"},
        {"name": "Dunbar", "short_name": "Dunbar", "number": "104"},
        {"name": "Edison", "short_name": "Edison", "number": "105"},
        {"name": "Emerson", "short_name": "Emerson", "number": "106"},
        {"name": "Garfield", "short_name": "Garfield", "number": "108"},
        {"name": "Magnet", "short_name": "Magnet", "number": "109"},
        {"name": "Heard", "short_name": "Heard", "number": "112"},
        {"name": "Herrera", "short_name": "Herrera", "number": "113"},
        {"name": "Kenilworth", "short_name": "Kenilworth", "number": "115"},
        {"name": "Lowell", "short_name": "Lowell", "number": "118"},
        {"name": "Monterey Park", "short_name": "Monterey Park", "number": "121"},
        {"name": "Shaw Montessori", "short_name": "Shaw", "number": "123"},
        {"name": "Faith North", "short_name": "Faith North", "number": "130"},
        {"name": "Emerson Court", "short_name": "Emerson Court", "number": "127"},
        {"name": "Plant Services", "short_name": "Plant Services", "number": "128"},
    ]

    for location in locations:
        loc = Location.objects.create(name=location["name"], short_name=location["short_name"], location_number=location["number"])
        loc.save()

    # Vendors
    vt = VendorType.objects.create(name="Retire/Rehire")
    vt.save()
    v = Vendor.objects.create(name="Educational Services, Inc.", short_name="ESI", vendor_type=vt)
    v.save()

    # Parse TalentEd
    # get_talented_xml()
    parse_hires()

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

    # Create Processes
    new_hire_process = Process.objects.create(name="New Hire Process")
    new_hire_process.save()

    contractor_process = Process.objects.create(name="New Contractor Process")
    contractor_process.save()

    ignore_process = Process.objects.create(name="Ignore Employee Process")
    ignore_process.save()

    # Create Tasks
    # Ignore Employee Step 1
    ignore_employee_task = Task.objects.create(name="Ignore Employee", task_function="task_dummy", task_type="User")
    ignore_employee_task.save()

    # Contractor Step 1
    select_contractor_services_task = Task.objects.create(name="Select Contractor Services", task_function="task_select_contractor_services", task_type="User")
    select_contractor_services_task.save()

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

    # Create Activities

    # Step 6 - TCP Fingerprinted
    tcp_fingerprint_employee_activity = Activity.objects.create(name="TCP Fingerprint Employee", process=new_hire_process)
    tcp_fingerprint_employee_activity.tasks.add(tcp_fingerprint_employee_task)
    tcp_fingerprint_employee_activity.users.add(tharris)
    tcp_fingerprint_employee_activity.users.add(mario)
    tcp_fingerprint_employee_activity.users.add(lauren)
    tcp_fingerprint_employee_activity.users.add(pat)
    tcp_fingerprint_employee_activity.users.add(claudia)
    tcp_fingerprint_employee_activity.save()

    tcp_fingerprint_contractor_activity = Activity.objects.create(name="TCP Fingerprint Contractor", process=contractor_process)
    tcp_fingerprint_contractor_activity.tasks.add(tcp_fingerprint_employee_task)
    tcp_fingerprint_contractor_activity.users.add(tharris)
    tcp_fingerprint_contractor_activity.users.add(mario)
    tcp_fingerprint_contractor_activity.users.add(lauren)
    tcp_fingerprint_contractor_activity.users.add(pat)
    tcp_fingerprint_contractor_activity.users.add(claudia)
    tcp_fingerprint_contractor_activity.save()

    # Step 5 - Onboarded
    onboard_employee_activity = Activity.objects.create(name="Onboard Employee", process=new_hire_process)
    onboard_employee_activity.tasks.add(onboard_employee_task)
    onboard_employee_activity.users.add(tharris)
    onboard_employee_activity.users.add(mario)
    onboard_employee_activity.users.add(lauren)
    onboard_employee_activity.users.add(pat)
    onboard_employee_activity.users.add(claudia)
    onboard_employee_activity.children.add(tcp_fingerprint_employee_activity)
    onboard_employee_activity.save()

    onboard_contractor_activity = Activity.objects.create(name="Onboard Contractor", process=contractor_process)
    onboard_contractor_activity.tasks.add(onboard_employee_task)
    onboard_contractor_activity.users.add(tharris)
    onboard_contractor_activity.users.add(mario)
    onboard_contractor_activity.users.add(lauren)
    onboard_contractor_activity.users.add(pat)
    onboard_contractor_activity.users.add(claudia)
    onboard_contractor_activity.children.add(tcp_fingerprint_contractor_activity)
    onboard_contractor_activity.save()

    # Step 4 - TCP Account
    create_tcp_account_activity = Activity.objects.create(name="Create TCP Account", process=new_hire_process)
    create_tcp_account_activity.tasks.add(create_tcp_account_task)
    create_tcp_account_activity.users.add(tharris)
    create_tcp_account_activity.users.add(frank)
    create_tcp_account_activity.users.add(matthew)
    create_tcp_account_activity.children.add(onboard_employee_activity)
    create_tcp_account_activity.save()

    create_contractor_tcp_account_activity = Activity.objects.create(name="Create Contractor TCP Account", process=contractor_process)
    create_contractor_tcp_account_activity.tasks.add(create_tcp_account_task)
    create_contractor_tcp_account_activity.users.add(tharris)
    create_contractor_tcp_account_activity.users.add(matthew)
    create_contractor_tcp_account_activity.users.add(frank)
    create_contractor_tcp_account_activity.children.add(onboard_contractor_activity)
    create_contractor_tcp_account_activity.save()

    # Step 3 - Parallel: Assign to Position (Employee Only), Synergy Account, AD Account
    assign_to_position_activity = Activity.objects.create(name="Assign Employee to Visions Position", process=new_hire_process)
    assign_to_position_activity.tasks.add(assign_to_position_task)
    assign_to_position_activity.users.add(tharris)
    assign_to_position_activity.users.add(matthew)
    assign_to_position_activity.users.add(frank)
    assign_to_position_activity.children.add(create_tcp_account_activity)
    assign_to_position_activity.save()

    create_ad_account_activity = Activity.objects.create(name="Create Active Directory Account", process=new_hire_process)
    create_ad_account_activity.tasks.add(create_ad_account_task)
    create_ad_account_activity.users.add(tharris)
    create_ad_account_activity.users.add(rocky)
    create_ad_account_activity.users.add(larhea)
    create_ad_account_activity.users.add(david)
    create_ad_account_activity.save()

    create_contractor_ad_account_activity = Activity.objects.create(name="Create Contractor Active Directory Account", process=contractor_process)
    create_contractor_ad_account_activity.tasks.add(create_ad_account_task)
    create_contractor_ad_account_activity.users.add(tharris)
    create_contractor_ad_account_activity.users.add(rocky)
    create_contractor_ad_account_activity.users.add(larhea)
    create_contractor_ad_account_activity.users.add(david)
    create_contractor_ad_account_activity.children.add(create_contractor_tcp_account_activity)
    create_contractor_ad_account_activity.save()

    create_synergy_account_activity = Activity.objects.create(name="Create Synergy Account", process=new_hire_process)
    create_synergy_account_activity.tasks.add(create_synergy_account_task)
    create_synergy_account_activity.users.add(marie)
    create_synergy_account_activity.users.add(paul)
    create_synergy_account_activity.users.add(tharris)
    create_synergy_account_activity.save()

    create_contractor_synergy_account_activity = Activity.objects.create(name="Create Contractor Synergy Account", process=contractor_process)
    create_contractor_synergy_account_activity.tasks.add(create_synergy_account_task)
    create_contractor_synergy_account_activity.users.add(tharris)
    create_contractor_synergy_account_activity.users.add(marie)
    create_contractor_synergy_account_activity.users.add(paul)
    create_contractor_synergy_account_activity.save()

    # Step 2
    create_visions_record_activity = Activity.objects.create(name="Create Employee Maintenance Record", process=new_hire_process)
    create_visions_record_activity.tasks.add(create_visions_record_task)
    create_visions_record_activity.users.add(tharris)
    create_visions_record_activity.users.add(lauren)
    create_visions_record_activity.users.add(mario)
    create_visions_record_activity.users.add(claudia)
    create_visions_record_activity.users.add(pat)
    create_visions_record_activity.children.add(assign_to_position_activity)
    create_visions_record_activity.children.add(create_ad_account_activity)
    create_visions_record_activity.children.add(create_synergy_account_activity)
    create_visions_record_activity.save()

    # Step 1
    create_epar_activity = Activity.objects.create(name="Create ePAR", process=new_hire_process)
    create_epar_activity.tasks.add(create_epar_task)
    create_epar_activity.users.add(tharris)
    create_epar_activity.users.add(lauren)
    create_epar_activity.users.add(mario)
    create_epar_activity.users.add(claudia)
    create_epar_activity.users.add(pat)
    create_epar_activity.children.add(create_visions_record_activity)
    create_epar_activity.save()

    # Contractor Step 1
    select_contractor_services = Activity.objects.create(name="Select Contractor Services", process=contractor_process)
    select_contractor_services.tasks.add(select_contractor_services_task)
    select_contractor_services.users.add(tharris)
    select_contractor_services.children.add(create_contractor_synergy_account_activity)
    select_contractor_services.children.add(create_contractor_ad_account_activity)
    select_contractor_services.save()

    # Ignore Employee Step 1
    ignore_employee_activity = Activity.objects.create(name="Ignore Employee", process=ignore_process)
    ignore_employee_activity.tasks.add(ignore_employee_task)
    ignore_employee_activity.users.add(tharris)
    ignore_employee_activity.users.add(lauren)
    ignore_employee_activity.save()

    # Add Start Activities to Processes
    new_hire_process.start_activity = create_epar_activity
    new_hire_process.save()

    contractor_process.start_activity = select_contractor_services
    contractor_process.save()

    ignore_process.start_activity = ignore_employee_activity
    ignore_process.save()
