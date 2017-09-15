from api.xml_parse import parse_hires
from bpm.xml_request import get_talented_xml
from django.conf import settings
import os


def run():
    path = settings.BASE_DIR + "/test.xml"
    if os.path.exists(path):
        os.remove(path)
    get_talented_xml()
    parse_hires()
