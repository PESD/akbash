from rest_framework import serializers
from django.contrib.auth.models import User
from bpm.models import Process, Activity, Workflow, WorkflowActivity, WorkflowTask, Task, TaskWorker, ProcessCategory
from api.models import Person
from api.serializers import PersonSerializer
from bpm.visions_helper import VisionsHelper
from django.core.exceptions import ObjectDoesNotExist


class WorkflowWithActivityData(object):
    completed_by = None
    completed_date = None

    def __init__(self, completed_by, completed_date):
        self.completed_by = completed_by
        self.completed_date = completed_date


class WorkflowWithActivity(object):
    id = None
    expanded = True
    label = None
    type = None
    data = None
    workflow_id = None
    children = None

    def __init__(self, id, label, type, data, workflow_id, children):
        self.id = id
        self.expanded = True
        self.label = label
        self.type = type
        self.data = data
        self.workflow_id = workflow_id
        self.children = children


def get_workflow_with_activity_from_workflow(workflow):
    wfa = WorkflowActivity.objects.get(workflow=workflow, activity=workflow.process.start_activity)
    if wfa.completed_by is not None:
        username = wfa.completed_by.username
    else:
        username = ""
    wfad = WorkflowWithActivityData(username, wfa.completed_date)
    return [WorkflowWithActivity(wfa.id, wfa.activity.name, wfa.status, wfad, workflow.id, wfa.activity.children)]


def get_workflow_with_activity_from_workflow_id_and_activity(workflow_id, activity):
    try:
        wfa = WorkflowActivity.objects.get(workflow__id=workflow_id, activity=activity)
        if wfa.completed_by is not None:
            username = wfa.completed_by.username
        else:
            username = ""
        wfad = WorkflowWithActivityData(username, wfa.completed_date)
        wwa = WorkflowWithActivity(wfa.id, wfa.activity.name, wfa.status, wfad, workflow_id, wfa.activity.children)
    except ObjectDoesNotExist:
        wwa = WorkflowWithActivity(0, activity.name, "Error", WorkflowWithActivityData(None, None), workflow_id, activity.children)
    return wwa


class CharListField(serializers.ListField):
    child = serializers.CharField()


class IntegerListField(serializers.ListField):
    child = serializers.IntegerField()


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        the_workflow_id = self.context.get("the_workflow_id")
        new_value = get_workflow_with_activity_from_workflow_id_and_activity(the_workflow_id, value)
        serializer = self.parent.parent.__class__(new_value, context=self.context)
        return serializer.data


class WorkflowWithActivityDataSerializer(serializers.Serializer):
    completed_by = serializers.CharField(max_length=256)
    completed_date = serializers.DateTimeField()


class WorkflowWithActivitySerializer(serializers.Serializer):
    label = serializers.CharField(max_length=256)
    type = serializers.CharField(max_length=256)
    expanded = serializers.BooleanField()
    data = WorkflowWithActivityDataSerializer(many=False)
    children = RecursiveField(many=True)


# Dashboard Stats Serializer
class DashboardStatsSerializer(serializers.Serializer):
    my_tasks = serializers.IntegerField()
    hires_this_month = serializers.IntegerField()
    active_workflows = serializers.IntegerField()


class GraphDataSetSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=255)
    data = IntegerListField()


class GraphSerializer(serializers.Serializer):
    labels = CharListField()
    datasets = GraphDataSetSerializer(many=True)


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


class ActivityNameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class ActivityChildrenField(serializers.RelatedField):
    def to_representation(self, value):
        return value.children


class ChildActivitySerializer(serializers.ModelSerializer):
    # children = RecursiveField(many=True)
    # label = serializers.CharField(source="name")
    activity = ActivityNameField(many=False, read_only=True)
    children = RecursiveField(many=False, source="activity")

    class Meta:
        model = WorkflowActivity
        fields = (
            "activity",
            "children",
        )


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
            "status",
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
    username = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        epar = validated_data["epar_id"]
        username = validated_data["username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "epar_id": epar,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "epar_id": epar, "username": username, "status": status, "message": message}


class TaskVisionsIDSerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    visions_id = serializers.IntegerField()
    username = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        visions_id = validated_data["visions_id"]
        username = validated_data["username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "visions_id": visions_id,
        }
        status, message = workflow_task.run_task(args)
        return {"workflow_task_id": workflow_task.id, "visions_id": visions_id, "username": username, "status": status, "message": message}


class TaskEmployeeADSerializer(serializers.Serializer):
    workflow_task_id = serializers.IntegerField()
    ad_username = serializers.CharField(max_length=50, allow_blank=True)
    username = serializers.CharField(max_length=50, allow_blank=True)
    status = serializers.BooleanField()
    message = serializers.CharField(max_length=200, allow_blank=True)

    def create(self, validated_data):
        workflow_task = WorkflowTask.objects.get(pk=validated_data["workflow_task_id"])
        username = validated_data["username"]
        ad_username = ""
        if validated_data["ad_username"] and validated_data["ad_username"] != "":
            ad_username = validated_data["ad_username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "ad_username": ad_username,
        }
        status, message = workflow_task.run_task(args)
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
        synergy_username = ""
        if validated_data["synergy_username"] and validated_data["synergy_username"] != "":
            synergy_username = validated_data["synergy_username"]
        args = {
            "workflow_task": workflow_task,
            "username": username,
            "status": validated_data["status"],
            "synergy_username": synergy_username,
        }
        status, message = workflow_task.run_task(args)
        if workflow_task.status == "Complete":
            employee = TaskWorker.get_employee_from_workflow_task(workflow_task)
            synergy_username = employee.get_synergy_username_or_blank()
        return {"workflow_task_id": workflow_task.id, "synergy_username": synergy_username, "username": username, "status": status, "message": message}


class TaskUpdateEmployeePosition(serializers.Serializer):
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


class TaskGenericCheck(serializers.Serializer):
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
