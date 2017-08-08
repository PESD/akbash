from bpm.models import Process, Task, Activity, Workflow, WorkflowActivity


def run():
    # Remove Badge Created Activity, Task and remove from workflow.
    badge_created_activity = Activity.objects.get(name="Employee Badge Printed")
    contractor_badge_created_activity = Activity.objects.get(name="Contractor Badge Printed")

    tcp_fingerprint_employee_activity = Activity.objects.get(name="TCP Fingerprint Employee")
    tcp_fingerprint_employee_activity.children.remove(badge_created_activity)
    tcp_fingerprint_employee_activity.save()

    tcp_fingerprint_contractor_activity = Activity.objects.get(name="TCP Fingerprint Contractor")
    tcp_fingerprint_contractor_activity.children.remove(contractor_badge_created_activity)
    tcp_fingerprint_contractor_activity.save()

    badge_created_activity.delete()
    contractor_badge_created_activity.delete()

    badge_created_task = Task.objects.get(name="Employee Badge Printed")
    badge_created_task.delete()
