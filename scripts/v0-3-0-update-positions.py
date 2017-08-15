from bpm.visions_helper import VisionsHelper
from api.models import Employee, Position, Location
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime


def update_position_from_employee(employee):
    visions_positions = VisionsHelper.get_positions_for_employee(employee.visions_id)
    if not visions_positions:
        return False
    secondary_positions = []
    no_primary = False
    try:
        primary_position = employee.positions.get(is_primary=True)
    except ObjectDoesNotExist:
        no_primary = True
    did_update = False
    for position in visions_positions:
        if position.position_ranking == "Primary":
            if no_primary:
                primary_position = Position.objects.create(person=employee, is_primary=True)
            location = VisionsHelper.get_position_location(position.dac)
            primary_position.title = position.description
            primary_position.visions_position_id = position.id
            primary_position.last_updated_by = "Visions"
            primary_position.last_updated_date = date.today()
            if location:
                primary_position.location = location
            primary_position.save()
            did_update = True
        else:
            secondary_positions.append(position)
    if secondary_positions:
        for secondary_position in secondary_positions:
            new_position = Position.objects.create(
                person=employee,
                title=secondary_position.description,
                visions_position_id=secondary_position.id,
                is_primary=False,
                last_updated_by="Visions",
                last_updated_date=date.today()
            )
            location = VisionsHelper.get_position_location(secondary_position.dac)
            if location:
                new_position.location = location
                new_position.save()
            did_update = True
    if did_update:
        return True
    return False


def run():
    employees = Employee.objects.exclude(visions_id__isnull=True)
    for employee in employees:
        update_position_from_employee(employee)
