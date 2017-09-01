from bpm.models import Process, ProcessCategory


def run():
    # new_hire_cat = ProcessCategory.objects.filter(name="New Hire")
    # existing_employee_cat = ProcessCategory.objects.filter(name="Existing Employee")
    # new_contractor_cat = ProcessCategory.objects.filter(name="New Contractor")

    # for cat in new_hire_cat:
    #     cat.delete()
    # for cat in existing_employee_cat:
    #     cat.delete()
    # for cat in new_contractor_cat:
    #     cat.delete()

    new_hire_cat = ProcessCategory.objects.create(name="New Hire", slug="new_hire")
    existing_employee_cat = ProcessCategory.objects.create(name="Existing Employee", slug="existing_employee")
    new_contractor_cat = ProcessCategory.objects.create(name="New Contractor", slug="new_contractor")

    new_hire_process = Process.objects.get(name="New Hire Process")
    new_hire_process.categories.add(new_hire_cat)
    new_hire_process.save()

    transfer_process = Process.objects.get(name="Transfer Process")
    transfer_process.categories.add(existing_employee_cat)
    transfer_process.save()

    termination_process = Process.objects.get(name="Termination Process")
    termination_process.categories.add(existing_employee_cat)
    termination_process.save()

    contractor_process = Process.objects.get(name="New Contractor Process")
    contractor_process.categories.add(new_contractor_cat)
    contractor_process.save()

    ignore_process = Process.objects.get(name="Ignore Employee Process")
    ignore_process.categories.add(new_hire_cat)
    ignore_process.save()
