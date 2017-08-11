from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from api import visions
from auditlog.models import ModelLog


# Function for updating data. Use this instead of updating objects directly
# in order to potentially capture in a future changelog/audit model.
def update_field(data_object, column, new_value, user=False):
    old_value = getattr(data_object, column)
    if new_value != old_value:
        # Save the new value. In the future could also call an
        # audit/changelog log function
        setattr(data_object, column, new_value)
        data_object.save()
        log = ModelLog.create_from_object(data_object, column, old_value, new_value)
        if user:
            log.user = user
            log.save()


# Vendor Classes
class VendorType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    vendor_type = models.ForeignKey(VendorType, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % self.name


# Person Classes

class Person(models.Model):
    TYPES = (
        ("Contractor", "Contractor"),
        ("Employee", "Employee"),
    )
    STATUSES = (
        ("newhire", "TalentEd New Hire"),
        ("inprocess", "In Process"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("visions", "Imported from Visions")
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="newhire")
    type = models.CharField(max_length=16, choices=TYPES)
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    badge_number = models.IntegerField(null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    race_white = models.BooleanField(default=False)
    race_asian = models.BooleanField(default=False)
    race_black = models.BooleanField(default=False)
    race_islander = models.BooleanField(default=False)
    race_american_indian = models.BooleanField(default=False)
    ethnicity = models.CharField(max_length=50, blank=True)
    hqt = models.CharField(max_length=16, blank=True)
    ssn = models.CharField(max_length=9, blank=True)
    tcp_id = models.IntegerField(null=True)
    talented_id = models.IntegerField(null=True)
    is_onboarded = models.BooleanField(default=False)
    onboarded_date = models.DateTimeField(null=True, blank=True)
    onboarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_tcp_fingerprinted = models.BooleanField(default=False)
    tcp_fingerprinted_date = models.DateTimeField(null=True, blank=True)
    tcp_fingerprinted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="tcp_fingerprinted_user")
    is_badge_created = models.BooleanField(default=False)
    badge_created_date = models.DateTimeField(null=True, blank=True)
    badge_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="badge_created_user")
    is_emp_record_created = models.BooleanField(default=False)
    emp_record_created_date = models.DateTimeField(null=True, blank=True)
    emp_record_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="emp_record_created_user")
    is_position_linked = models.BooleanField(default=False)
    position_linked_date = models.DateTimeField(null=True, blank=True)
    position_linked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="position_linked_user")
    is_visions_account_needed = models.BooleanField(default=False)
    is_visions_account_created = models.BooleanField(default=False)
    visions_account_created_date = models.DateTimeField(null=True, blank=True)
    visions_account_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="visions_account_created_user")
    is_synergy_account_needed = models.BooleanField(default=False)
    is_synergy_account_created = models.BooleanField(default=False)
    synergy_account_created_date = models.DateTimeField(null=True, blank=True)
    synergy_account_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="synergy_account_created_user")
    is_ad_account_created = models.BooleanField(default=False)
    ad_account_created_date = models.DateTimeField(null=True, blank=True)
    ad_account_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ad_account_created_user")
    is_cell_phone_needed = models.BooleanField(default=False)
    is_cell_phone_created = models.BooleanField(default=False)
    cell_phone_created_date = models.DateTimeField(null=True, blank=True)
    cell_phone_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cell_phone_created_user")
    is_desk_phone_created = models.BooleanField(default=False)
    desk_phone_created_date = models.DateTimeField(null=True, blank=True)
    desk_phone_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="desk_phone_created_user")
    start_date = models.DateField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=255, blank=True)
    last_updated_date = models.DateTimeField(null=True, blank=True, auto_now=True)

    # Convieniece function to verify if an Employee exists by talented_id
    @staticmethod
    def person_exists(tid):
        qs = Person.objects.filter(talented_id=tid)
        if qs.exists():
            return True
        else:
            return False

    def personType(self):
        try:
            if self.contractor.id:
                return "Contractor"
        except ObjectDoesNotExist:
            return "Employee"

    def generate_badge(self):
        max_badge = Person.objects.all().aggregate(Max('badge_number'))['badge_number__max']
        if not max_badge:
            max_badge = 11000
        badge = max_badge + 1
        self.badge_number = badge
        self.save()
        return self.badge_number

    def update_ad_service(self, ad_username, created_by):
        self.is_ad_account_created = True
        self.ad_account_created_by = created_by
        if self.services.filter(type="ad"):
            ad_service = self.services.get(type="ad")
            update_field(ad_service, "user_info", ad_username, created_by)
        else:
            ad_service = self.services.create(type="ad", person=self, user_info=ad_username)
            ad_service.save()
        if ad_service.user_info == ad_username:
            self.save()
            return True
        return False

    def update_synergy_service(self, synergy_username, created_by):
        self.is_synergy_account_created = True
        self.synergy_account_created_by = created_by
        self.is_synergy_account_needed = True
        if self.services.filter(type="synergy"):
            synergy_service = self.services.get(type="synergy")
            update_field(synergy_service, "user_info", synergy_username, created_by)
        else:
            synergy_service = self.services.create(type="synergy", person=self, user_info=synergy_username)
            synergy_service.save()
        if synergy_service.user_info == synergy_username:
            self.save()
            return True
        return False

    def get_ad_username_or_blank(self):
        try:
            ad_service = self.services.get(type="ad")
            return ad_service.user_info
        except ObjectDoesNotExist:
            return ""

    def get_synergy_username_or_blank(self):
        try:
            synergy_service = self.services.get(type="synergy")
            return synergy_service.user_info
        except ObjectDoesNotExist:
            return ""


class Employee(Person):
    employee_id = models.CharField(max_length=7, blank=True)
    visions_id = models.IntegerField(null=True, blank=True)
    sub_type = models.CharField(max_length=1, blank=True)
    marked_as_hired = models.DateField(null=True, blank=True)
    epar_id = models.IntegerField(null=True, blank=True)

    def update_employee_from_visions(self):
        visions_user = User.objects.get(username="visions")
        update_field(self, "employee_id", visions.Viwpremployees().EmployeeID(self.visions_id), visions_user)
        update_field(self, "first_name", visions.Viwpremployees().FirstName(self.visions_id), visions_user)
        update_field(self, "last_name", visions.Viwpremployees().LastName(self.visions_id), visions_user)
        update_field(self, "middle_name", visions.Viwpremployees().MiddleName(self.visions_id), visions_user)
        update_field(self, "birth_date", visions.Viwpremployees().BirthDate(self.visions_id), visions_user)
        update_field(self, "start_date", visions.Viwpremployees().HireDate(self.visions_id), visions_user)
        update_field(self, "ssn", visions.Viwpremployees().EmployeeSSN(self.visions_id), visions_user)
        ethnicity = visions.Viwpremployees().PREthnicOrigin(self.visions_id)
        clean_ethnicity = False
        if ethnicity == "Not Hispanic or Latino":
            clean_ethnicity = "Non-Hispanic"
        if ethnicity == "Hispanic or Latino":
            clean_ethnicity = "Hispanic"
        if clean_ethnicity:
            update_field(self, "ethnicity", clean_ethnicity, visions_user)
        race = visions.Viwpremployees().tblHRMasterEthnicityID(self.visions_id)
        if race == 1:
            update_field(self, "race_white", True, visions_user)
            update_field(self, "race_black", False, visions_user)
            update_field(self, "race_american_indian", False, visions_user)
            update_field(self, "race_asian", False, visions_user)
            update_field(self, "race_islander", False, visions_user)
        if race == 2:
            update_field(self, "race_white", False, visions_user)
            update_field(self, "race_black", True, visions_user)
            update_field(self, "race_american_indian", False, visions_user)
            update_field(self, "race_asian", False, visions_user)
            update_field(self, "race_islander", False, visions_user)
        if race == 3:
            update_field(self, "race_white", True, visions_user)
            update_field(self, "race_black", False, visions_user)
            update_field(self, "race_american_indian", False, visions_user)
            update_field(self, "race_asian", False, visions_user)
            update_field(self, "race_islander", False, visions_user)
        if race == 4:
            update_field(self, "race_white", False, visions_user)
            update_field(self, "race_black", False, visions_user)
            update_field(self, "race_american_indian", True, visions_user)
            update_field(self, "race_asian", False, visions_user)
            update_field(self, "race_islander", False, visions_user)
        if race == 5:
            update_field(self, "race_white", False, visions_user)
            update_field(self, "race_black", False, visions_user)
            update_field(self, "race_american_indian", False, visions_user)
            update_field(self, "race_asian", True, visions_user)
            update_field(self, "race_islander", False, visions_user)
        if race == 6:
            update_field(self, "race_white", False, visions_user)
            update_field(self, "race_black", False, visions_user)
            update_field(self, "race_american_indian", False, visions_user)
            update_field(self, "race_asian", False, visions_user)
            update_field(self, "race_islander", True, visions_user)
        gender = visions.Viwpremployees().Gender(self.visions_id)
        if gender == 1:
            update_field(self, "gender", "M", visions_user)
        if gender == 2:
            update_field(self, "gender", "F", visions_user)

    def update_employee_from_epar(self):
        pass

    @staticmethod
    def should_import_employee(employee):
        try:
            if Employee.objects.get(ssn=employee.ssn):
                return False
        except ObjectDoesNotExist:
            pass
        try:
            if Employee.objects.get(first_name=employee.first_name, last_name=employee.last_name):
                return False
        except ObjectDoesNotExist:
            pass
        try:
            if Employee.objects.get(visions_id=employee.id):
                return False
        except ObjectDoesNotExist:
            pass
        return True


class Contractor(Person):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class HireDateRange(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


# Service Classes

class Service(models.Model):
    TYPES = (
        ("visions", "Visions"),
        ("synergy", "Synergy"),
        ("ad", "Active Directory"),
        ("cell", "Cell Phone"),
        ("phone", "Desk Phone")
    )
    type = models.CharField(max_length=16, choices=TYPES)
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="services",
    )
    user_info = models.CharField(max_length=50)

    # There can be only one service of each type per Person
    class Meta:
        unique_together = ("type", "person")

    def __unicode__(self):
        return '%s: %s' % (self.type, self.user_data)


# Organizational Classes

class Location(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    location_number = models.CharField(max_length=3)


class Department(models.Model):
    name = models.CharField(max_length=255)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)


# Position Classes

class PositionType(models.Model):
    position_type_desc = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    classification = models.CharField(max_length=50)
    is_contracted = models.BooleanField()


class Position(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="positions")
    position_type = models.ForeignKey(PositionType, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    visions_position_id = models.IntegerField(null=True)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=255, blank=True)

    def position_exists_for_user(person):
        positions = Position.objects.filter(person__id=person.id)
        if positions.exists():
            return True
        else:
            return False


# Comments

class Comment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
