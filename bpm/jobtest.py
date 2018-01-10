from akjob.models import Job, JobCallable
from api.models import Person
from datetime import timedelta


class JobTest():
    def run():
        troy = Person.objects.get(first_name="Troy")
        troy.first_name = "Troyyy"
        troy.save()
