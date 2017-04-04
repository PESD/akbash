from rest_framework import serializers
from api.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='employee-detail', format='html')

    class Meta:
        model = Employee
        fields = (
            "api_url",
            "employee_id",
            "first_name",
            "last_name",
            "middle_name",
            "badge_number",
            "birth_date",
            "gender",
            "race_white",
            "race_asian",
            "race_black",
            "race_islander",
            "race_american_indian",
            "ethnicity",
            "hqt",
            "ssn",
            "tcp_id",
            "talented_id",
            "onboarding_date",
            "is_tcp_fingerprinted",
            "is_badge_created",
            "visions_id",
            "sub_type",
            "marked_as_hired",
            "epar_id",
        )
