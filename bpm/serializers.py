from rest_framework import serializers
from django.contrib.auth.models import User
from bpm.models import Process, Activity, Workflow, WorkflowActivity, WorkflowTask, Task, TaskWorker, ProcessCategory
from api.models import Person
from api.serializers import PersonSerializer
from bpm.visions_helper import VisionsHelper


class UserSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='user-detail', format='html')

    class Meta:
        model = User
        fields = (
            "api_url",
            "id",
            "username",
        )


class ActivitySerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='activity-detail', format='html')
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = (
            "api_url",
            "id",
            "name",
            "users",
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('users')
        return queryset


class ProcessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessCategory
        fields = (
            "slug"
        )


class ProcessSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='process-detail', format='html')
    start_activity = ActivitySerializer(many=False, read_only=True)

    class Meta:
        model = Process
        fields = (
            "api_url",
            "id",
            "name",
            "start_activity",
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('start_activity')
        return queryset


class WorkflowSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflow-detail', format='html')

    class Meta:
        model = Workflow
        fields = (
            "api_url",
            "id",
            "process",
            "person",
        )


class TaskSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='task-detail', format='html')

    class Meta:
        model = Task
        fields = (
            "api_url",
            "id",
            "name",
            "task_function",
            "task_type",
        )


class WorkflowTaskSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflowtask-detail', format='html')
    task = TaskSerializer(many=False, read_only=True)

    class Meta:
        model = WorkflowTask
        fields = (
            "api_url",
            "id",
            "status",
            "task",
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('task')
        return queryset


class WorkflowActivitySerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflowactivity-detail', format='html')
    activity = ActivitySerializer(many=False, read_only=True)
    workflow_tasks = WorkflowTaskSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowActivity
        fields = (
            "api_url",
            "id",
            "status",
            "workflow",
            "activity",
            "workflow_tasks",
        )

    @staticmethod
    def setup_eager_loading(queryset):
            """ Perform necessary eager loading of data. """
            queryset = queryset.select_related('activity')
            queryset = queryset.prefetch_related('workflow_tasks')
            return queryset


class WorkflowCompleteSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflow-detail', format='html')
    person = PersonSerializer(many=False, read_only=True)
    process = ProcessSerializer(many=False, read_only=True)
    workflow_activites = WorkflowActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = (
            "api_url",
            "id",
            "process",
            "person",
            "workflow_activites",
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('person')
        queryset = queryset.select_related('process')
        queryset = queryset.prefetch_related('workflow_activites', 'workflow_activites__workflow_tasks', 'person__services')
        return queryset


class CreateWorkflowSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()
    person_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        process_id = validated_data["process_id"]
        person_id = validated_data["person_id"]
        process = Process.objects.get(pk=process_id)
        person = Person.objects.get(pk=person_id)
        status, message = process.start_workflow(person)
        return {"process_id": process_id, "person_id": person_id, "status": status, "message": message}


# Visions Serializers
class EparSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200, allow_blank=True)
    position_title = serializers.CharField(max_length=200, allow_blank=True)


class VisionsEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200, allow_blank=True)


# Task Serializers
class TaskEparSerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    epar_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        epar = validated_data["epar_id"]
        args = {
            "workflow_task": workflow_task,
            "epar_id": epar
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "epar_id": epar, "status": status, "message": message}


class TaskVisionsIDSerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    visions_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        visions_id = validated_data["visions_id"]
        args = {
            "workflow_task": workflow_task,
            "visions_id": visions_id
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "visions_id": visions_id, "status": status, "message": message}


class TaskEmployeeADSerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    ad_username = serializers.CharField(max_length=50, allow_blank=True)
    username = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        username = validated_data["username"]
        args = {
            "workflow_task": workflow_task,
            "username": username
        }
        status, message = workflow_task.run_task(args)
        ad_username = ""
        return {"workflow_task_id": workflow_task.id, "ad_username": ad_username, "username": username, "status": status, "message": message}


class TaskEmployeeSynergySerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    synergy_username = serializers.CharField(max_length=50, allow_blank=True)
    username = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        username = validated_data["username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "status": validated_data["status"],
        }
        status, message = workflow_task.run_task(args)
        synergy_username = ""
        if workflow_task.status == "Complete":
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            synergy_username = employee.get_synergy_username_or_blank()
        return {"workflow_task_id": workflow_task.id, "synergy_username": synergy_username, "username": username, "status": status, "message": message}


class TaskUpdateEmployeePosition(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        args = {
            "workflow_task": workflow_task,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "status": status, "message": message}


class TaskGenericCheck(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        args = {
            "workflow_task": workflow_task,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "status": status, "message": message}


class TaskGenericTodo(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)
    username = serializers.CharField(max_length=50, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        username = validated_data["username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "status": status, "message": message, "username": username}


class TaskWorkLocations(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)
    username = serializers.CharField(max_length=50, allow_blank=True)
    locations = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        username = validated_data["username"]
        locations = validated_data["locations"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "locations": locations,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "status": status, "message": message, "username": username, "locations": locations}
