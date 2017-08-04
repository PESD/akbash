from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ModelLog (models.Model):
    model_id = models.IntegerField()
    model_module = models.CharField(max_length=255)
    model_class = models.CharField(max_length=255)
    model_field_name = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    change_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @staticmethod
    def get_module_from_object(object):
        return object.__module__

    @staticmethod
    def get_class_from_object(object):
        return object.__class__.__name__

    @classmethod
    def create_from_object(cls, object, field, old_value, new_value):
        module_string = cls.get_module_from_object(object)
        class_string = cls.get_class_from_object(object)
        if not old_value:
            old_value = ""
        if not new_value:
            new_value = ""
        return cls.objects.create(
            model_id=object.pk,
            model_module=module_string,
            model_class=class_string,
            model_field_name=field,
            old_value=str(old_value),
            new_value=str(new_value),
        )
