from rest_framework import serializers
from auditlog.models import ModelLog


class ModelLogSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = ModelLog
        fields = (
            "model_id",
            "model_module",
            "model_class",
            "model_field_name",
            "old_value",
            "new_value",
            "change_date",
            "user",
        )
