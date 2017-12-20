from rest_framework import serializers
from api.models import (
    Employee,
    Service,
    Contractor,
    Vendor,
    Position,
    Location,
    Department,
    PositionType,
    Person,
    Comment,
    VisionsPositions,
    update_field,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(view_name='user-detail', format='html')

    class Meta:
        model = User
        fields = (
            "api_url",
            "id",
            "username",
        )


# As of now, Services are never directly exposed through REST
# This serializer is used to expose Services in the EmployeeSerializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "type",
            "user_info",
            "status",
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

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('vendor_type')
        return queryset


# The following serializers are exposed in the API
class PersonSerializer(serializers.ModelSerializer):
    # Expose the URL to access employee-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='employee-detail', format='html')
    # Expose the usernames of various workflow update fields
    onboarded_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    tcp_fingerprinted_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    badge_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    emp_record_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    position_linked_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    visions_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    synergy_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    ad_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    locations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='short_name')
    status = serializers.SerializerMethodField()

    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            "api_url",
            "id",
            "type",
            "status",
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
            "long_term_sub",
            "long_term_sub_replacing",
            "tcp_id",
            "talented_id",
            "is_onboarded",
            "onboarded_date",
            "onboarded_by",
            "is_tcp_fingerprinted",
            "tcp_fingerprinted_date",
            "tcp_fingerprinted_by",
            "is_badge_created",
            "badge_created_date",
            "badge_created_by",
            "is_emp_record_created",
            "emp_record_created_date",
            "emp_record_created_by",
            "is_position_linked",
            "position_linked_date",
            "position_linked_by",
            "is_visions_account_needed",
            "is_visions_account_created",
            "visions_account_created_date",
            "visions_account_created_by",
            "is_synergy_account_needed",
            "is_synergy_account_created",
            "synergy_account_created_date",
            "synergy_account_created_by",
            "is_ad_account_created",
            "ad_account_created_date",
            "ad_account_created_by",
            "is_cell_phone_needed",
            "is_cell_phone_created",
            "cell_phone_created_date",
            "cell_phone_created_by",
            "is_desk_phone_created",
            "desk_phone_created_date",
            "desk_phone_created_by",
            "services",
            "start_date",
            "last_updated_by",
            "last_updated_date",
            "locations",
        )

    def get_status(self, obj):
        return obj.get_status_display()

    def update(self, instance, validated_data):
        user = False
        if validated_data.get("last_updated_by", False):
            user = User.objects.get(username=validated_data["last_updated_by"])
        update_field(instance, 'first_name', validated_data.get('first_name', instance.first_name), user)
        update_field(instance, 'last_name', validated_data.get('last_name', instance.last_name), user)
        update_field(instance, 'middle_name', validated_data.get('middle_name', instance.middle_name), user)
        update_field(instance, 'badge_number', validated_data.get('badge_number', instance.badge_number), user)
        update_field(instance, 'birth_date', validated_data.get('birth_date', instance.birth_date), user)
        update_field(instance, 'gender', validated_data.get('gender', instance.gender), user)
        update_field(instance, 'race_white', validated_data.get('race_white', instance.race_white), user)
        update_field(instance, 'race_asian', validated_data.get('race_asian', instance.race_asian), user)
        update_field(instance, 'race_black', validated_data.get('race_black', instance.race_black), user)
        update_field(instance, 'race_islander', validated_data.get('race_islander', instance.race_islander), user)
        update_field(instance, 'race_american_indian', validated_data.get('race_american_indian', instance.race_american_indian), user)
        update_field(instance, 'ethnicity', validated_data.get('ethnicity', instance.ethnicity), user)
        update_field(instance, 'hqt', validated_data.get('hqt', instance.hqt), user)
        update_field(instance, 'ssn', validated_data.get('ssn', instance.ssn), user)
        update_field(instance, 'tcp_id', validated_data.get('tcp_id', instance.tcp_id), user)
        update_field(instance, 'talented_id', validated_data.get('talented_id', instance.talented_id), user)
        update_field(instance, 'start_date', validated_data.get('start_date', instance.start_date), user)
        instance.refresh_from_db()
        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('onboarded_by')
        queryset = queryset.select_related('tcp_fingerprinted_by')
        queryset = queryset.select_related('badge_created_by')
        queryset = queryset.select_related('emp_record_created_by')
        queryset = queryset.select_related('position_linked_by')
        queryset = queryset.select_related('visions_account_created_by')
        queryset = queryset.select_related('synergy_account_created_by')
        queryset = queryset.select_related('ad_account_created_by')
        queryset = queryset.prefetch_related('services')
        return queryset


class EmployeeSerializer(serializers.ModelSerializer):
    # Expose the URL to access employee-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='employee-detail', format='html')
    # Expose the usernames of various workflow update fields
    onboarded_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    tcp_fingerprinted_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    badge_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    emp_record_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    position_linked_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    visions_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    synergy_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    ad_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    status = serializers.SerializerMethodField()

    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = (
            "api_url",
            "id",
            "type",
            "status",
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
            "long_term_sub",
            "long_term_sub_replacing",
            "tcp_id",
            "talented_id",
            "visions_id",
            "sub_type",
            "marked_as_hired",
            "epar_id",
            "transfer_epar_id",
            "termination_epar_id",
            "is_onboarded",
            "onboarded_date",
            "onboarded_by",
            "is_tcp_fingerprinted",
            "tcp_fingerprinted_date",
            "tcp_fingerprinted_by",
            "is_badge_created",
            "badge_created_date",
            "badge_created_by",
            "is_emp_record_created",
            "emp_record_created_date",
            "emp_record_created_by",
            "is_position_linked",
            "position_linked_date",
            "position_linked_by",
            "is_visions_account_needed",
            "is_visions_account_created",
            "visions_account_created_date",
            "visions_account_created_by",
            "is_synergy_account_needed",
            "is_synergy_account_created",
            "synergy_account_created_date",
            "synergy_account_created_by",
            "is_ad_account_created",
            "ad_account_created_date",
            "ad_account_created_by",
            "is_cell_phone_needed",
            "is_cell_phone_created",
            "cell_phone_created_date",
            "cell_phone_created_by",
            "is_desk_phone_created",
            "desk_phone_created_date",
            "desk_phone_created_by",
            "services",
            "start_date",
        )

    def get_status(self, obj):
        return obj.get_status_display()

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('onboarded_by')
        queryset = queryset.select_related('tcp_fingerprinted_by')
        queryset = queryset.select_related('badge_created_by')
        queryset = queryset.select_related('emp_record_created_by')
        queryset = queryset.select_related('position_linked_by')
        queryset = queryset.select_related('visions_account_created_by')
        queryset = queryset.select_related('synergy_account_created_by')
        queryset = queryset.select_related('ad_account_created_by')
        queryset = queryset.prefetch_related('services')
        return queryset


class ContractorSerializer(serializers.ModelSerializer):
    # Expose the URL to access contractor-detail
    api_url = serializers.HyperlinkedIdentityField(view_name='contractor-detail', format='html')
    # Expose the usernames of various workflow update fields
    onboarded_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    tcp_fingerprinted_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    badge_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    emp_record_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    position_linked_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    visions_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    synergy_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    ad_account_created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    # Will pull in any Service usernames (Visions, Synergy, etc)
    services = ServiceSerializer(many=True, read_only=True)
    # vendor = VendorSerializer(many=False, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Contractor
        fields = (
            "api_url",
            "id",
            "type",
            "status",
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
            "long_term_sub",
            "long_term_sub_replacing",
            "tcp_id",
            "talented_id",
            "is_onboarded",
            "onboarded_date",
            "onboarded_by",
            "is_tcp_fingerprinted",
            "tcp_fingerprinted_date",
            "tcp_fingerprinted_by",
            "is_badge_created",
            "badge_created_date",
            "badge_created_by",
            "is_emp_record_created",
            "emp_record_created_date",
            "emp_record_created_by",
            "is_position_linked",
            "position_linked_date",
            "position_linked_by",
            "is_visions_account_created",
            "visions_account_created_date",
            "visions_account_created_by",
            "is_synergy_account_created",
            "is_synergy_account_needed",
            "synergy_account_created_date",
            "synergy_account_created_by",
            "is_ad_account_created",
            "ad_account_created_date",
            "ad_account_created_by",
            "services",
            "vendor",
            "start_date",
        )

    def get_status(self, obj):
        return obj.get_status_display()

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('onboarded_by')
        queryset = queryset.select_related('tcp_fingerprinted_by')
        queryset = queryset.select_related('badge_created_by')
        queryset = queryset.select_related('emp_record_created_by')
        queryset = queryset.select_related('position_linked_by')
        queryset = queryset.select_related('visions_account_created_by')
        queryset = queryset.select_related('synergy_account_created_by')
        queryset = queryset.select_related('ad_account_created_by')
        queryset = queryset.prefetch_related('services')
        return queryset


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


class VisionsPositionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisionsPositions
        fields = (
            "id",
            "description",
            "type",
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
    location = LocationSerializer(many=False, read_only=False)
    department = DepartmentSerializer(many=False, read_only=True)
    position_type = PositionTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Position
        fields = (
            "api_url",
            "id",
            "title",
            "is_primary",
            "person",
            "last_updated_date",
            "last_updated_by",
            "location",
            "department",
            "position_type",
        )

    def create(self, validated_data):
        print(validated_data)
        location_data = validated_data.pop('location')
        location_number = location_data["location_number"]
        location = Location.objects.get(location_number=location_number)
        position = Position.objects.create(**validated_data)
        position.location = location
        position.save()
        return position

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('location')
        queryset = queryset.select_related('department')
        queryset = queryset.select_related('position_type')
        return queryset


class PositionSkinnySerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=False, read_only=True, slug_field='short_name')

    class Meta:
        model = Position
        fields = (
            "id",
            "title",
            "location",
        )


class PersonSkinnySerializer(serializers.ModelSerializer):
    positions = PositionSkinnySerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            "id",
            "type",
            "status",
            "first_name",
            "last_name",
            "long_term_sub",
            "long_term_sub_replacing",
            "start_date",
            "positions",
        )

    def get_status(self, obj):
        return obj.get_status_display()

    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('positions', 'positions__location')
        return queryset


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "person",
            "text",
            "user",
            "created_date",
        )
