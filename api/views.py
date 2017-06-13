from api.models import Employee, Contractor, Position, Location, Department, PositionType, Person
from api.serializers import EmployeeSerializer, ContractorSerializer, PositionSerializer, LocationSerializer, DepartmentSerializer, PositionTypeSerializer, PersonSerializer
from bpm.models import Workflow
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import viewsets


# The api_root simply displays an HTML page with any root API end-points
# that are exposed
@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        'employees': reverse('employee-list', request=request, format=format)
    })


# ModelViewSet does all of the heavy lifting for REST framework.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class EmployeeNoWorkflowViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.exclude(
        id__in=Workflow.objects.all().values_list('person')
    )
    serializer_class = EmployeeSerializer


class ContractorViewSet(viewsets.ModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PositionTypeViewSet(viewsets.ModelViewSet):
    queryset = PositionType.objects.all()
    serializer_class = PositionTypeSerializer
