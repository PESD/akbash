from django.test import TestCase
from akbash_core.models import Person, Employee, update_field
from akbash_core.xml_parse import parse_hires


# Create your tests here.
class PersonTestCase(TestCase):
    def setUp(self):
        jon = Employee.objects.create(first_name="Jon", last_name="Snow")
        arya = Person.objects.create(first_name="Arya", last_name="Stark")
        jon.employee_id = "SN12345"
        jon.talented_id = 12345
        jon.save()
        arya.save()

    def test_find_employee(self):
        people = Person.objects.all()
        self.assertEqual(people.count(), 2)
        newjon = Employee.objects.get(first_name="Jon")
        self.assertEqual(newjon.employee_id, "SN12345")

    def test_person_exists(self):
        self.assertIs(Person.person_exists(12345), True)

    def test_update_field(self):
        update_jon = Employee.objects.get(talented_id=12345)
        update_field(update_jon, "middle_name", "Stark")
        final_jon = Employee.objects.get(talented_id=12345)
        self.assertEqual(final_jon.middle_name, "Stark")

    def test_parse_hires(self):
        parse_hires()
        hodor = Employee.objects.get(first_name="Hodor1")
        self.assertEqual(hodor.first_name, "Hodor1")
        hodor_32 = Employee.objects.get(first_name="Hodor32")
        self.assertEqual(hodor_32.first_name, "Hodor32")
