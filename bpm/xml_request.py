import requests
from django.conf import settings


def get_talented_xml():
    talented_key = settings.TALENTED_API_KEY

    post_vars = {
        "sStartDate": "20170101000000",
        "sEndDate": "20170320000000",
        "sKey": talented_key,
    }
    r = requests.post("https://phxschools.tedk12.com/hire/nfIntegration/srApplicantExport.asmx/RetrieveHiresXML", data=post_vars)
    print("after")
    # file_path = os.path.join(os.pardir, "test.xml")
    file_path = "test.xml"
    xml_file = open(file_path, "w")
    xml_file.truncate()
    xml_file.write(r.text)
    xml_file.close()
