from bpm.models import Process, Activity, Workflow, WorkflowActivity, Task, WorkflowTask
from api.models import Person


def get_children(activity, workflow):
    children = []
    for activity in activity.children.all():
        children.append(WorkflowActivity.objects.get(workflow=workflow, activity=activity))
    return children


def run():
    print("Starting test....")
    person = Person.objects.get(first_name="RUDOLPH")
    print("Fetched a person: " + person.first_name + " " + person.last_name)
    workflow = person.current_workflow
    print("Fetched the current Workflow: " + workflow.process.name)
    start_activity = workflow.process.start_activity
    print("Start Activity is: " + start_activity.name)
    current_wa = [WorkflowActivity.objects.get(workflow=workflow, activity=start_activity)]
    keep_going = True
    level = 0
    level_tracker = {}
    level_tracker[level] = False
    while keep_going:
        for wa in current_wa:
            print("Level: " + str(level) + " Activity: " + wa.activity.name)
            current_wa = get_children(wa.activity, workflow)
            if current_wa != []:
                level_tracker[level] = True
        if level_tracker[level]:
            level = level + 1
            level_tracker[level] = False
        else:
            keep_going = False
