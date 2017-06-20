from rest_framework import serializers
from django.contrib.auth.models import User
from bpm.models import Process, Activity, Workflow, WorkflowActivity, WorkflowTask, Task, TaskWorker
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


class CreateWorkflowSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()
    person_id = serializers.IntegerField()

    def create(self, validated_data):
        process = Process.objects.get(pk=validated_data["process_id"])
        person = Person.objects.get(pk=validated_data["person_id"])
        return process.start_workflow(person)


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
        if workflow_task.status == "Complete":
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                workflow_activity.advance_workflow_activity()
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
        if workflow_task.status == "Complete":
            workflow_activities = workflow_task.workflowactivity_set.all()
            for workflow_activity in workflow_activities:
                workflow_activity.advance_workflow_activity()
        return {"workflow_task_id": workflow_task.id, "visions_id": visions_id, "status": status, "message": message}
