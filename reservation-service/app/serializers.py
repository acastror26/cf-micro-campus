from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, ResourceType, Resource, Reservation, UserPermission

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class UserPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPermission
        fields = ['is_staff', 'is_admin', 'user_service_id', 'user_data']
        read_only_fields = ['user_service_id']

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(required=False)
    is_admin = serializers.BooleanField(required=False)
    user_service_id = serializers.CharField(max_length=255, required=False, read_only=True)
    phone_number = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_admin', 'user_service_id', 'phone_number', 'country', 'state', 'city', 'password']
        read_only_fields = ['id', 'user_service_id']

    def _handle_user(self, validated_data, action='create', instance=None):
        data = {}
        if 'first_name' in validated_data:
            data['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            data['last_name'] = validated_data.pop('last_name')
        data['email'] = validated_data.pop('email')
        data['username'] = data['email']
        data['is_active'] = validated_data.pop('is_active', False)
        if action == 'create':
            return super().create(data)
        data.pop('email', None)
        data.pop('username', None)
        return super().update(instance, data)

    def _handle_permission(self, instance, validated_data):
        user_data = {}
        print(validated_data)
        if 'phone_number' in validated_data:
            user_data['phone_number'] = validated_data.pop('phone_number')
        if 'country' in validated_data:
            user_data['country'] = validated_data.pop('country')
        if 'state' in validated_data:
            user_data['state'] = validated_data.pop('state')
        if 'city' in validated_data:
            user_data['city'] = validated_data.pop('city')
        user_service_id = validated_data.pop('user_service_id')
        
        permission_data = {
            'is_staff': validated_data.pop('is_staff', False),
            'is_admin': validated_data.pop('is_admin', False),
            'user_data': user_data,
        }

        permission, _ = UserPermission.objects.get_or_create(user=instance, user_service_id=user_service_id)
        for key, value in permission_data.items():
            if value is not None and getattr(permission, key) != value:
                setattr(permission, key, value)
        permission.save()

    def create(self, validated_data):
        validated_data.pop('password', None)
        user = self._handle_user(validated_data)
        # Do not save passwords in this service
        user.set_unusable_password()
        user.save()
        self._handle_permission(user, validated_data)
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        instance = self._handle_user(validated_data, action='update', instance=instance)
        self._handle_permission(instance, validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        permission = UserPermission.objects.get(user=instance)
        representation['is_staff'] = permission.is_staff
        representation['is_admin'] = permission.is_admin
        representation['user_service_id'] = permission.user_service_id
        representation.update(permission.user_data)
        return representation
