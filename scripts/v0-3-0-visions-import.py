from bpm.visions_helper import VisionsHelper
from api.models import Employee


def run():
    employees = VisionsHelper.get_employees_for_import()
    for employee in employees:
        new_employee = Employee.objects.create(
            first_name=employee.first_name,
            last_name=employee.last_name,
            ssn=employee.ssn,
            visions_id=employee.id,
            status="visions"
        )
    all_employees = Employee.objects.all()
    for an_employee in all_employees:
        if an_employee.visions_id:
            an_employee.update_employee_from_visions()
