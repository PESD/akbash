import xml.etree.ElementTree as ET
# import urllib2
from .models import Person, Employee, update_field


# xml_file = urllib2.urlopen("https://phxschools.tedk12.com/hire/nfIntegration/srApplicantExport.asmx/RetrieveHiresXML?sStartDate=20170101000000&sEndDate=20170320000000&sKey=680iv19L72ta1SN47t00888iG26L1H3I")
def parse_hires():
    xml_file = "RetrieveHiresXML.xml"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    hodor_int = 1

    for newhire in root:
        emp_info = newhire.find("EmployeeInfo")
        app_id = emp_info.find("ApplicantId")
        tid = int(app_id.find("IdValue").text)

        if Person.person_exists(tid) is False:
            hire = Employee.objects.create(talented_id=tid)
        else:
            hire = Employee.objects.get(talented_id=tid)

        hodor = "Hodor%i" % (hodor_int)

        update_field(hire, "first_name", hodor)

        hodor_int = hodor_int + 1
