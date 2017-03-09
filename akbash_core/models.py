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
    badge_number = models.IntegerField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)
    race = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    hqt = models.CharField(max_length=16)
    ssn = models.CharField(max_length=9)
    tcp_id = models.IntegerField()
    onboarding_date = models.DateTimeField()
    is_tcp_fingerprinted = models.BooleanField()
    is_badge_created = models.BooleanField()


class Employee(Person):
    employee_id = models.CharField(max_length=7)
    visions_id = models.IntegerField()
    sub_type = models.CharField(max_length=1)
    marked_as_hired = models.DateField()
    epar_id = models.IntegerField()


class Contractor(Person):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class HireDateRange(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


# Service Classes

class Service(models.Model):
    name = models.CharField(max_length=255)


class Visions(Service):
    username = models.CharField(max_length=50)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)


class Synergy(Service):
    username = models.CharField(max_length=50)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)


class ActiveDirectory(Service):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)


class CellPhone(Service):
    cell_number = models.CharField(max_length=10)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)


class DeskPhone(Service):
    desk_phone = models.CharField(max_length=10)
    extension = models.CharField(max_length=4)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)


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
