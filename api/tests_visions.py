
import api.visions
from django.conf import settings
from django.test import TestCase


# Override api.visions settings to use default database instead of visions DB.
api.visions.cstring = (
    'DSN=' + settings.DATABASES['default']['OPTIONS']['dsn'] +
    ';PWD=' + settings.DATABASES['default']['PASSWORD'] +
    ';DATABASE=' + settings.DATABASES['default']['NAME'] +
    ';UID=' + settings.DATABASES['default']['USER']
)


class VisionsTestCase(TestCase):
    "Setup data for api.visions test cases."
    pass


class ExecSQLTestCase(VisionsTestCase):
    "Test api.visions.exec_sql."
    pass
