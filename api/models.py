from django.db import models


# Vendor Classes

class VendorType(models.Model):
    name = models.CharField(max_length=255)


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    vendor_type = models.ForeignKey(VendorType, on_delete=models.CASCADE)


# Person Classes

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    badge_number = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    race_white = models.BooleanField(default=False)
    race_asian = models.BooleanField(default=False)
    race_black = models.BooleanField(default=False)
    race_islander = models.BooleanField(default=False)
    race_american_indian = models.BooleanField(default=False)
    ethnicity = models.CharField(max_length=50)
    hqt = models.CharField(max_length=16)
    ssn = models.CharField(max_length=9)
    tcp_id = models.IntegerField(null=True, blank=True)
    talented_id = models.IntegerField(null=True, blank=True)
    onboarding_date = models.DateTimeField(null=True, blank=True)
    is_tcp_fingerprinted = models.BooleanField(default=False)
    is_badge_created = models.BooleanField(default=False)

    @staticmethod
    def person_exists(tid):
        qs = Person.objects.filter(talented_id=tid)
        if qs.exists():
            return True
        else:
            return False


class Employee(Person):
    employee_id = models.CharField(max_length=7)
    visions_id = models.IntegerField(null=True, blank=True)
    sub_type = models.CharField(max_length=1)
    marked_as_hired = models.DateField(null=True, blank=True)
    epar_id = models.IntegerField(null=True, blank=True)


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
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position_type = models.ForeignKey(PositionType, on_delete=models.CASCADE)


# Function for updating data

def update_field(data_object, column, new_value):
    old_value = getattr(data_object, column)
    if new_value != old_value:
        # Save the new value. In the future could also call an
        # audit log function
        setattr(data_object, column, new_value)
        data_object.save()
