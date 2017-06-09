from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from bpm.serializers import UserSerializer, ActivitySerializer, ProcessSerializer, WorkflowSerializer, WorkflowActivitySerializer, CreateWorkflowSerializer, WorkflowCompleteSerializer
from bpm.models import Process, Activity, Workflow, WorkflowActivity
from django.contrib.auth.models import User


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        'processes': reverse('process-list', request=request, format=format)
    })


# ModelViewSet does all of the heavy lifting for REST framework.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFromUsernameViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.parser_context['kwargs']['username']
        return User.objects.filter(username=username)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkflowCompleteViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowCompleteSerializer


class WorkflowActivityViewSet(viewsets.ModelViewSet):
    queryset = WorkflowActivity.objects.all()
    serializer_class = WorkflowActivitySerializer


class WorkflowActivityActiveUserViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowActivitySerializer

    def get_queryset(self):
        user_id = self.request.parser_context['kwargs']['user_id']
        return WorkflowActivity.objects.filter(status="Active").filter(activity__users__id=user_id)


class WorkflowFromWorkflowActivityViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer

    def get_queryset(self):
        workflowactivity_id = self.request.parser_context['kwargs']['workflowactivity_id']
        return Workflow.objects.filter(workflow_activites__id__contains=workflowactivity_id)


class WorkflowFromPersonViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer

    def get_queryset(self):
        person_id = self.request.parser_context['kwargs']['person_id']
        return Workflow.objects.filter(person__id=person_id)


class WorkflowCompleteFromActiveUserViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowCompleteSerializer

    def get_queryset(self):
        user_id = self.request.parser_context['kwargs']['user_id']
        wf_activities = WorkflowActivity.objects.filter(status="Active").filter(activity__users__id=user_id)
        workflow_list = []
        for wfa in wf_activities:
            workflow_list.append(wfa.workflow.id)
        workflow_dedupped = list(set(workflow_list))
        return Workflow.objects.filter(id__in=workflow_dedupped)


class WorkflowCompleteActiveViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowCompleteSerializer

    def get_queryset(self):
        wf_activities = WorkflowActivity.objects.filter(status="Active")
        workflow_list = []
        for wfa in wf_activities:
            workflow_list.append(wfa.workflow.id)
        workflow_dedupped = list(set(workflow_list))
        return Workflow.objects.filter(id__in=workflow_dedupped)


@csrf_exempt
def create_workflow_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateWorkflowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
