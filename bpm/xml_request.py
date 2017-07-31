import requests
import os
from django.conf import settings


def get_talented_xml():
    # We store the TalentEd API key in our private settings file.
    # Unless this is Circle CI running, then we store it in a private /
    # / environment var
    if os.environ.get("CIRCLECI") == "true":
        talented_key = os.environ.get("TALENTEDAPI")
    else:
        talented_key = settings.TALENTED_API_KEY

    # The date range we pull New Hires for. We need to not hard code this.
    post_vars = {
        "sStartDate": "20170101000000",
        "sEndDate": "20180630000000",
        "sKey": talented_key,
    }

    # The TalentEd URL. Move this to settings?
    r = requests.post("https://phxschools.tedk12.com/hire/nfIntegration/srApplicantExport.asmx/RetrieveHiresXML", data=post_vars)

    # Right now we simply save the xml file in akbash root as test.xml. Need to think of a better solution.
    file_path = settings.BASE_DIR + "/test.xml"
    xml_file = open(file_path, "w")
    xml_file.truncate()
    xml_file.write(r.text)
    xml_file.close()
