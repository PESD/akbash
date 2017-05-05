from rest_framework import serializers
from api.models import Employee, Service, Contractor, Vendor


# As of now, Services are never directly exposed through REST
# This serializer is used to expose Services in the EmployeeSerializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "type",
            "user_info"
        )


class VendorSerializer(serializers.ModelSerializer):
    vendor_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Vendor
        fields = (
            "name",
            "short_name",
            "vendor_type",
        )


class EmployeeSerializer(serializers.ModelSerializer):
    # Expose the URL to access employee-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='employee-detail', format='html')

    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)

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
            "services",
        )


class ContractorSerializer(serializers.ModelSerializer):
    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)
    vendor = VendorSerializer(many=False, read_only=True)

    class Meta:
        model = Contractor
        fields = (
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
            "services",
            "vendor",
        )
