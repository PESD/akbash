from bpm.models import Workflow


def run():
    workflows = Workflow.objects.filter(status="Active")
    for workflow in workflows:
        person = workflow.person
        person.current_workflow = workflow
        person.save()
