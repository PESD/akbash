from bpm.models import Task


def run():
    user_task_names = [
        "Create ePAR",
        "Create Employee Maintenance Record",
        "Create Termination ePAR",
        "Create Transfer ePAR",
        "Transfer Active Directory Account",
        "Transfer Synergy Account",
    ]
    observer_task_names = [
        "Create TCP Account",
    ]
    user_tasks = Task.objects.filter(name__in=user_task_names)
    observer_tasks = Task.objects.filter(name__in=observer_task_names)

    for user_task in user_tasks:
        user_task.task_type = "User"
        user_task.save()

    for observer_task in observer_tasks:
        observer_task.task_type = "Observer"
        observer_task.save()
