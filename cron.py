import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akbash.settings")
django.setup()

from bpm.xml_request import get_talented_xml
from api.xml_parse import parse_hires

get_talented_xml()
parse_hires()
