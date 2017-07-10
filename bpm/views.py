from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from bpm.serializers import (UserSerializer,
                             ActivitySerializer,
                             ProcessSerializer,
                             WorkflowSerializer,
                             WorkflowActivitySerializer,
                             CreateWorkflowSerializer,
                             WorkflowCompleteSerializer,
                             WorkflowTaskSerializer,
                             EparSerializer,
                             VisionsEmployeeSerializer,
                             TaskSerializer,
                             TaskEparSerializer,
                             TaskVisionsIDSerializer,
                             TaskEmployeeADSerializer,
                             TaskUpdateEmployeePosition,
                             TaskGenericCheck,
                             TaskGenericTodo,
                             )
from bpm.models import (Process,
                        Activity,
                        Workflow,
                        WorkflowActivity,
                        WorkflowTask,
                        Task,
                        )
from bpm.visions_helper import VisionsHelper
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


class WorkflowActivityFromActiveWorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowActivitySerializer

    def get_queryset(self):
        workflow_id = self.request.parser_context['kwargs']['workflow_id']
        return WorkflowActivity.objects.filter(status="Active").filter(workflow__id=workflow_id)


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
        username = self.request.parser_context['kwargs']['username']
        wf_activities = WorkflowActivity.objects.filter(status="Active").filter(activity__users__username=username)
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


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkflowTaskViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTask.objects.all()
    serializer_class = WorkflowTaskSerializer


@csrf_exempt
def create_workflow_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateWorkflowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Visions Views
class EparViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = EparSerializer

    def list(self, request):
        epars = VisionsHelper.get_all_epars()
        serializer = EparSerializer(instance=epars, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        epar = VisionsHelper.get_epar(pk)
        serializer = EparSerializer(instance=epar)
        return Response(serializer.data)


class VisionsEmployeeViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = VisionsEmployeeSerializer

    def list(self, request):
        employees = VisionsHelper.get_all_employees()
        serializer = VisionsEmployeeSerializer(instance=employees, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        employee = VisionsHelper.get_employee(pk)
        serializer = VisionsEmployeeSerializer(instance=employee)
        return Response(serializer.data)


# Task Views
@csrf_exempt
def task_set_epar_id_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskEparSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_set_visions_id_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskVisionsIDSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_check_employee_ad_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskEmployeeADSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_update_position_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskUpdateEmployeePosition(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_generic_check_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskGenericCheck(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_generic_todo_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskGenericTodo(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
