import requests
from bpm.api_keys import keys
import os
from .signals.signals import talented_signal


def get_talented_xml():
    print("test")
    post_vars = {
        "sStartDate": "20170101000000",
        "sEndDate": "20170320000000",
        "sKey": keys["talented"]["sKey"],
    }
    r = requests.post("https://phxschools.tedk12.com/hire/nfIntegration/srApplicantExport.asmx/RetrieveHiresXML", data=post_vars)
    print("after")
    # file_path = os.path.join(os.pardir, "test.xml")
    file_path = "test.xml"
    print(file_path)
    xml_file = open(file_path, "w")
    xml_file.truncate()
    xml_file.write(r.text)
    xml_file.close()
