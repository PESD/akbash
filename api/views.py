from api.models import Employee, Contractor, Position, Location, Department, PositionType, Person, Vendor, Comment
from api.serializers import (EmployeeSerializer,
                             ContractorSerializer,
                             PositionSerializer,
                             LocationSerializer,
                             DepartmentSerializer,
                             PositionTypeSerializer,
                             PersonSerializer,
                             VendorSerializer,
                             CommentSerializer,
                             UserSerializer,
                             )
from bpm.models import Workflow
from django.contrib.auth.models import User
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


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


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


class PositionFromPersonViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return Position.objects.filter(person__id=person_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentFromPersonViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return Comment.objects.filter(person__id=person_id)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
