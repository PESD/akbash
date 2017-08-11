from api.models import Employee
from bpm.synergy_helper import SynergyHelper
from django.contrib.auth.models import User


def run():
    all_employees = Employee.objects.all()
    tandem = User.objects.get(username="tandem")
    for an_employee in all_employees:
        if an_employee.visions_id:
            # Update Synergy username if found
            synergy_username = SynergyHelper.get_synergy_login(an_employee.visions_id)
            if synergy_username:
                an_employee.update_synergy_service(synergy_username, tandem)
