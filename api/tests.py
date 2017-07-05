from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Person, Employee, update_field, Service, Vendor, VendorType, Contractor
from api.xml_parse import parse_hires
from bpm.xml_request import get_talented_xml
from datetime import date
from api.serializers import EmployeeSerializer, ContractorSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.utils.six import BytesIO
import os


# Create your tests here.
class PersonTestCase(TestCase):
    def setUp(self):
        # Add a couple of Employees to use in the tests.
        jon = Employee.objects.create(first_name="Jon", last_name="Snow")
        arya = Person.objects.create(first_name="Arya", last_name="Stark")
        jon.employee_id = "SN12345"
        jon.talented_id = 12345
        sansa_user = User.objects.create_user('sstark', 'sstark@winterfell.com', 'lady')
        sansa_user.save()
        jon.save()
        arya.save()

    def test_find_employee(self):
        # Can we find the Jon Snow employee we created?
        people = Person.objects.all()
        self.assertEqual(people.count(), 2)
        newjon = Employee.objects.get(first_name="Jon")
        self.assertEqual(newjon.employee_id, "SN12345")

    def test_person_exists(self):
        # Does our person_exists() model function work?
        self.assertIs(Person.person_exists(12345), True)

    def test_update_field(self):
        # Does our custom update function work?
        update_jon = Employee.objects.get(talented_id=12345)
        update_field(update_jon, "middle_name", "Stark")
        final_jon = Employee.objects.get(talented_id=12345)
        self.assertEqual(final_jon.middle_name, "Stark")

    def test_parse_hires(self):
        # Can we parse through the TalentEd New Hire XML file?
        # If running on Circle CI, we must also pull down the file.
        if os.environ.get("CIRCLECI") == "true":
            get_talented_xml()
        parse_hires()
        emp = Employee.objects.get(talented_id=13345)
        self.assertEqual(emp.first_name, "Yenni")
        self.assertEqual(emp.ethnicity, "Hispanic")
        self.assertIs(emp.race_asian, False)
        self.assertEqual(emp.gender, "F")
        self.assertEqual(emp.marked_as_hired, date(2017, 1, 23))
        emp2 = Employee.objects.get(talented_id=13475)
        self.assertEqual(emp2.first_name, "Berhana")
        self.assertIs(emp2.race_white, False)
        emp3 = Employee.objects.get(talented_id=13325)
        self.assertEqual(emp3.first_name, "Jennifer")
        self.assertIs(emp3.race_white, True)
        self.assertIs(emp.race_asian, False)

    def test_services(self):
        arya = Person.objects.get(first_name="Arya")
        sansa = User.objects.get(username="sstark")
        arya.update_ad_service("arya.stark", sansa)
        ad_arya = arya.services.get(type='ad')
        self.assertEqual(ad_arya.user_info, 'arya.stark')
        arya.update_ad_service("a.stark", sansa)
        ad_arya = arya.services.get(type='ad')
        self.assertEqual(ad_arya.user_info, 'a.stark')


class RestTestCase(TestCase):
    def setUp(self):
        # Set up some data to test REST functionality. Start with Employee
        tyrion = Employee.objects.create(first_name="Tyrion", last_name="Lanister")
        tyrion.save()
        visions = Service.objects.create(type="visions", person=tyrion, user_info="tlanister")
        visions.save()
        synergy = Service.objects.create(type="synergy", person=tyrion, user_info="tyrion")
        synergy.save()
        # Now set up test data to test Contractor
        castle = VendorType.objects.create(name="castle")
        castle.save()
        winterfell = Vendor.objects.create(name="Winterfell", short_name="WinFell", vendor_type=castle)
        winterfell.save()
        ned = Contractor.objects.create(first_name="Ned", last_name="Stark", vendor=winterfell)
        ned.save()
        ned_visions = Service.objects.create(type="visions", person=ned, user_info="nstark")
        ned_visions.save()

    def test_json(self):
        # Serialize an Employee object to JSON then parse it to an object.
        # Since we are not actually making an HTTP request, we must fake /
        # / it using APIRequestFactory()
        factory = APIRequestFactory()
        request = factory.get('/api/')
        serializer_context = {
            'request': Request(request),
        }
        tyrion = Employee.objects.get(first_name="Tyrion")
        t_serial = EmployeeSerializer(instance=tyrion, context=serializer_context)
        json_string = JSONRenderer().render(t_serial.data)
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        # Check the object created by the JSON parser. Did it come through as expected?
        self.assertEqual(data["first_name"], "Tyrion")
        # Now lets loop through services and pull out the Visions user.
        vuser = ""
        for a in data["services"]:
            if a["type"] == "visions":
                vuser = a["user_info"]
        # Did we find a Visions user and is it as expected?
        self.assertEqual(vuser, "tlanister")

    def test_contractor_json(self):
        # Serialize a Contractor object to JSON then parse it to an object.
        # Since we are not actually making an HTTP request, we must fake /
        # / it using APIRequestFactory()
        factory = APIRequestFactory()
        request = factory.get('/api/')
        serializer_context = {
            'request': Request(request),
        }
        ned = Contractor.objects.get(first_name="Ned")
        n_serial = ContractorSerializer(instance=ned, context=serializer_context)
        json_string = JSONRenderer().render(n_serial.data)
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        self.assertEqual(data["first_name"], "Ned")
        # Make sure the Vendor information came over properly
        vendor = Vendor.objects.get(id=data["vendor"])
        self.assertEqual(data["vendor"], vendor.id)
        self.assertEqual(vendor.name, "Winterfell")
        self.assertEqual(vendor.vendor_type.name, "castle")
        # Check services for good measure
        self.assertEqual(data["services"][0]["user_info"], "nstark")
