from api.models import Employee
from api.serializers import EmployeeSerializer
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
