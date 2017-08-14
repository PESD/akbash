from django.contrib.auth.models import User
from bpm.visions_helper import VisionsHelper
from bpm.synergy_helper import SynergyHelper
from api import ldap
from api.models import Employee


def run():
    employees = VisionsHelper.get_employees_for_import()
    for employee in employees:
        new_employee = Employee.objects.create(
            first_name=employee.first_name,
            last_name=employee.last_name,
            ssn=employee.ssn,
            visions_id=employee.id,
            status="visions",
            type="Employee",
        )
    all_employees = Employee.objects.all()
    tandem = User.objects.get(username="tandem")
    for an_employee in all_employees:
        if an_employee.visions_id:
            # Update demographics from Visions
            an_employee.update_employee_from_visions()
            # Update Synergy username if found
            synergy_username = SynergyHelper.get_synergy_login(an_employee.visions_id)
            if synergy_username:
                an_employee.update_synergy_service(synergy_username, tandem)
            # Update Active Directory if found
            ad_username = ldap.get_ad_username_from_visions_id(an_employee.visions_id)
            if ad_username:
                an_employee.update_ad_service(ad_username, tandem)
