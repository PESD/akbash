from api.models import Employee
from api.serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import viewsets


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        'employees': reverse('employee-list', request=request, format=format)
    })


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
