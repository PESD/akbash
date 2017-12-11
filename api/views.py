from datetime import datetime
from api.models import (
    Employee,
    Contractor,
    Position, Location,
    Department,
    PositionType,
    Person,
    Vendor,
    Comment,
    VisionsPositions,
)
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
                             PersonSkinnySerializer,
                             VisionsPositionsSerializer,
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
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer

    def get_queryset(self):
        queryset = Person.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonMissedStartDateViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSkinnySerializer

    def get_queryset(self):
        queryset = Person.objects.filter(
            start_date__lte=datetime.today(),
            status="inprocess",
            current_workflow__process__name__in=["New Hire Process", "Transfer Process"]
        ).exclude(start_date__isnull=True).order_by("start_date")
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonAllContractorsViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer

    def get_queryset(self):
        queryset = Person.objects.filter(type="Contractor")
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonAllEmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSkinnySerializer

    def get_queryset(self):
        queryset = Person.objects.filter(type="Employee")
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonAllLongTermSubsViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSkinnySerializer

    def get_queryset(self):
        queryset = Person.objects.filter(long_term_sub=True)
        return self.get_serializer_class().setup_eager_loading(queryset)


class PersonFromWorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSkinnySerializer

    def get_queryset(self):
        workflow_id = self.request.parser_context['kwargs']['workflow_id']
        return Person.objects.filter(workflow__id=workflow_id)


class EmployeeNoWorkflowViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.exclude(
        id__in=Workflow.objects.all().values_list('person')
    )
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.exclude(
            id__in=Workflow.objects.all().values_list('person')
        )
        return self.get_serializer_class().setup_eager_loading(queryset)


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer

    def get_queryset(self):
        queryset = Vendor.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class ContractorViewSet(viewsets.ModelViewSet):
    serializer_class = ContractorSerializer

    def get_queryset(self):
        queryset = Contractor.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        queryset = Position.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationFromPerson(viewsets.ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return Location.objects.filter(person__pk=person_id)


class LocationNotFromPerson(viewsets.ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return Location.objects.exclude(person__pk=person_id)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class VisionsPositionsViewSet(viewsets.ModelViewSet):
    queryset = VisionsPositions.objects.all()
    serializer_class = VisionsPositionsSerializer


class PositionTypeViewSet(viewsets.ModelViewSet):
    queryset = PositionType.objects.all()
    serializer_class = PositionTypeSerializer


class PositionFromPersonViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        queryset = Position.objects.filter(person__id=person_id)
        return self.get_serializer_class().setup_eager_loading(queryset)


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
