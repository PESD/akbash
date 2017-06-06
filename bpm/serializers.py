from rest_framework import serializers
from django.contrib.auth.models import User
from bpm.models import Process, Activity, Workflow, WorkflowActivity
from api.models import Person
from api.serializers import PersonSerializer


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


class WorkflowCompleteSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflow-detail', format='html')
    person = PersonSerializer(many=False, read_only=True)
    process = ProcessSerializer(many=False, read_only=True)

    class Meta:
        model = Workflow
        fields = (
            "api_url",
            "id",
            "process",
            "person",
        )


class WorkflowActivitySerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='workflowactivity-detail', format='html')

    class Meta:
        model = WorkflowActivity
        fields = (
            "api_url",
            "id",
            "status",
            "workflow",
            "activity",
        )


class CreateWorkflowSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()
    person_id = serializers.IntegerField()

    def create(self, validated_data):
        process = Process.objects.get(pk=validated_data["process_id"])
        person = Person.objects.get(pk=validated_data["person_id"])
        return process.start_workflow(person)
