from rest_framework import serializers
from api.models import Employee, Service, Contractor, Vendor, Position, Location, Department, PositionType


# As of now, Services are never directly exposed through REST
# This serializer is used to expose Services in the EmployeeSerializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "type",
            "user_info",
        )


# As of now, Vendors are never directly exposed through REST
# This serializer is used to expose Vendor in the ContractorSerializer
class VendorSerializer(serializers.ModelSerializer):
    vendor_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Vendor
        fields = (
            "id",
            "name",
            "short_name",
            "vendor_type",
        )


# The following serializers are exposed in the API
class EmployeeSerializer(serializers.ModelSerializer):
    # Expose the URL to access employee-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='employee-detail', format='html')

    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = (
            "api_url",
            "id",
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
    # Expose the URL to access contractor-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='contractor-detail', format='html')
    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)
    vendor = VendorSerializer(many=False, read_only=True)

    class Meta:
        model = Contractor
        fields = (
            "api_url",
            "id",
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


class LocationSerializer(serializers.ModelSerializer):
    # Expose the URL to access position-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='location-detail', format='html')

    class Meta:
        model = Location
        fields = (
            "api_url",
            "id",
            "name",
            "short_name",
            "location_number",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    # Expose the URL to access department-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='department-detail', format='html')

    class Meta:
        model = Department
        fields = (
            "api_url",
            "id",
            "name",
            "supervisor",
        )


class PositionTypeSerializer(serializers.ModelSerializer):
    # Expose the URL to access position-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='position-type-detail', format='html')

    class Meta:
        model = PositionType
        fields = (
            "api_url",
            "id",
            "position_type_desc",
            "position_name",
            "classification",
            "is_contracted",
        )


class PositionSerializer(serializers.ModelSerializer):
    # Expose the URL to access position-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='position-detail', format='html')
    location = LocationSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)
    position_type = PositionTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Position
        fields = (
            "api_url",
            "id",
            "location",
            "department",
            "position_type",
        )