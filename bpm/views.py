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
                             TaskEmployeeSynergySerializer,
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
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class ProcessViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessSerializer

    def get_queryset(self):
        queryset = Process.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkflowCompleteViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowCompleteSerializer

    def get_queryset(self):
        queryset = Workflow.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class WorkflowCompleteCompletedViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowCompleteSerializer

    def get_queryset(self):
        queryset = Workflow.objects.filter(status="Complete").exclude(process__name="Ignore Employee Process")
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class WorkflowActivityViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowActivitySerializer

    def get_queryset(self):
        queryset = WorkflowActivity.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class WorkflowActivityFromActiveWorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowActivitySerializer

    def get_queryset(self):
        workflow_id = self.request.parser_context['kwargs']['workflow_id']
        queryset = WorkflowActivity.objects.filter(status="Active").filter(workflow__id=workflow_id)
        return self.get_serializer_class().setup_eager_loading(queryset)


class WorkflowActivityActiveUserViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowActivitySerializer

    def get_queryset(self):
        user_id = self.request.parser_context['kwargs']['user_id']
        queryset = WorkflowActivity.objects.filter(status="Active").filter(activity__users__id=user_id)
        return self.get_serializer_class().setup_eager_loading(queryset)


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
        queryset = Workflow.objects.filter(id__in=workflow_dedupped).filter(status="Active")
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class WorkflowCompleteActiveViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowCompleteSerializer

    def get_queryset(self):
        queryset = Workflow.objects.filter(status="Active")
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkflowTaskViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowTaskSerializer

    def get_queryset(self):
        queryset = WorkflowTask.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


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
def task_check_employee_synergy_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskEmployeeSynergySerializer(data=data, partial=True)
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
