from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, ResourceType, Resource, Reservation, UserPermission

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
        fields = ['is_staff', 'is_admin']

class UserSerializer(serializers.ModelSerializer):
    user_permission = UserPermissionSerializer(many=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_permission']

    def update(self, instance, validated_data):
        user_permission_data = validated_data.pop('user_permission')
        instance = super().update(instance, validated_data)
        
        if user_permission_data:
            user_permission, _ = UserPermission.objects.get_or_create(user=instance)
            user_permission.is_staff = user_permission_data.get('is_staff', user_permission.is_staff)
            user_permission.is_admin = user_permission_data.get('is_admin', user_permission.is_admin)
            user_permission.save()
