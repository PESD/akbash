from rest_framework import viewsets
from auditlog.models import ModelLog
from auditlog.serializers import ModelLogSerializer


# Create your views here.
class ModelLogViewSet(viewsets.ModelViewSet):
    queryset = ModelLog.objects.all()
    serializer_class = ModelLogSerializer


class ModelLogByPersonViewSet(viewsets.ModelViewSet):
    serializer_class = ModelLogSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return ModelLog.objects.filter(model_class__in=["Person", "Employee"], model_id=person_id).order_by('-change_date')
