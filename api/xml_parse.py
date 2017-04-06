import xml.etree.ElementTree as ET
from .models import Person, Employee, update_field
from datetime import date
import os


# Django doesn't allow null strings, so must convert any None objects
# to empty strings.
def get_xml_text(xml_object):
    if xml_object is None:
        return ""
    else:
        return xml_object.text


# Map TalentEd races strings to our model's boolean races.
def get_race(xml_object):
    race_dict = {}
    races = ["RaceWhite", "RaceBlack", "RaceAsian", "RaceIslander", "RaceAmericanIndian"]
    for race in races:
        race_text = get_xml_text(xml_object.find(race))
        if race_text == "T":
            race_dict[race] = True
        else:
            race_dict[race] = False
    return race_dict


# Translate TalentEd date to python date()
def date_from_talented(date_string):
    if "-" in date_string:
        date_arr = date_string.split("-")
        return date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
    else:
        return date(1900, 1, 1)


# Strip out hyphons in SSNs
def format_ssn(ssn):
    return ssn.replace("-", "")


# TalentEd genders: 1 = Male, 2 = Female
def gender_from_talented(gender):
    if gender == "1":
        return "M"
    elif gender == "2":
        return "F"
    else:
        return ""


# Am now just reading from a file. bpm.xml_request module handles downloading the file
# Need to find a better location for the XML file to be saved (and rotated)
# Also, all of this code should probably be moved to a future 'etl' app.

def parse_hires():
    # Simply reads test.xml from the root akbash directory. Obviously this needs to change.
    xml_file = "test.xml"
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Loop through each new hire in the TalentEd XML file.
    for newhire in root:
        emp_info = newhire.find("EmployeeInfo")
        app_id = emp_info.find("ApplicantId")
        tid = int(app_id.find("IdValue").text)

        # Do we create a new Employee or update an existing?
        if Person.person_exists(tid) is False:
            hire = Employee.objects.create(talented_id=tid)
        else:
            hire = Employee.objects.get(talented_id=tid)

        # Name
        name_info = emp_info.find("PersonName")
        update_field(hire, "first_name", get_xml_text(name_info.find("GivenName")))
        update_field(hire, "last_name", get_xml_text(name_info.find("FamilyName")))

        # Ethnicity
        desc_info = emp_info.find("PersonDescriptors")
        demo_info = desc_info.find("DemographicDescriptors")
        update_field(hire, "ethnicity", get_xml_text(demo_info.find("Ethnicity")))

        # Race
        race_dict = get_race(demo_info)
        update_field(hire, "race_american_indian", race_dict["RaceAmericanIndian"])
        update_field(hire, "race_white", race_dict["RaceWhite"])
        update_field(hire, "race_asian", race_dict["RaceAsian"])
        update_field(hire, "race_black", race_dict["RaceBlack"])
        update_field(hire, "race_islander", race_dict["RaceIslander"])

        # Birth Date
        bio_info = desc_info.find("BiologicalDescriptors")
        birth_text = get_xml_text(bio_info.find("DateOfBirth"))
        birth_date = date_from_talented(birth_text)
        if birth_date != date(1900, 1, 1):
            update_field(hire, "birth_date", birth_date)

        # Gender
        gender_code = get_xml_text(bio_info.find("GenderCode"))
        gender = gender_from_talented(gender_code)
        if gender != "":
            update_field(hire, "gender", gender)

        # SSN
        legal_info = desc_info.find("LegalIdentifiers")
        id_tag = legal_info.find(".//PersonLegalId[@documentType='Social Security Card']")
        ssn = get_xml_text(id_tag.find("IdValue"))
        ssn_clean = format_ssn(ssn)
        update_field(hire, "ssn", ssn_clean)

        # Marked as Hired DateOfBirth
        pos_info = newhire.find("PositionInfo")
        offer_info = pos_info.find("OfferInfo")
        hire_string = get_xml_text(offer_info.find("DateJobAccepted"))
        hire_date = date_from_talented(hire_string)
        if hire_date != date(1900, 1, 1):
            update_field(hire, "marked_as_hired", hire_date)
