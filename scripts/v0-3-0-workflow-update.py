from bpm.models import Workflow, Process


def run():
    ignore_employee = Process.objects.get(name="Ignore Employee Process")
    workflows = Workflow.objects.filter(status="Active").exclude(process=ignore_employee)
    for workflow in workflows:
        person = workflow.person
        person.status = "inprocess"
        person.save()
    completed_workflows = Workflow.objects.filter(status="Complete").exclude(process=ignore_employee)
    for workflow in completed_workflows:
        person = workflow.person
        person.status = "active"
        person.save()
