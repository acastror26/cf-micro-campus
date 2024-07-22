from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Room, ResourceType, Resource, Reservation, UserPermission
from .serializers import RoomSerializer, ResourceTypeSerializer, ResourceSerializer, ReservationSerializer, UserSerializer
from .permissions import IsApplicationStaff, IsApplicationAdminOrRequestingUser, IsApplicationAdmin, IsApplicationAdminOrSameUser, IsApplicationStaffOrRequestingUser

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsApplicationAdmin()]
        return super().get_permissions()

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsApplicationAdmin()]
        return super().get_permissions()

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsApplicationStaff()]
        elif self.request.method == 'DELETE':
            return [IsApplicationAdmin()]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsApplicationAdminOrRequestingUser()]
        elif self.action == 'partial_update':
            return [IsApplicationStaffOrRequestingUser()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        permission = user.permission
        if permission and permission.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(requesting_user=user)

    def perform_create(self, serializer):
        serializer.save(requesting_user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        permission = user.permission
        is_staff = permission and permission.is_staff
        if instance.status == Reservation.APPROVED:
            raise ValueError('Cannot update an approved reservation')
        if is_staff and instance.requesting_user != user:
            if instance.status == Reservation.DENIED:
                raise ValueError('Cannot update the status of a denied reservation')
            if set(serializer.validated_data.keys()) != {'status'}:
                raise ValueError('Only status of other users\' reservations can be updated by staff')
            serializer.save(approver_user=user, status=serializer.validated_data['status'])
        serializer.save(status=Reservation.REVIEW_PENDING)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        is_admin = user.permission and user.permission.is_admin
        if not is_admin and (instance.status == Reservation.APPROVED or instance.status == Reservation.DENIED):
            raise ValueError('Cannot delete an approved or denied reservation')
        return super().destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsApplicationAdmin()]
        elif self.request.method in ['POST', 'PUT']:
            return [IsApplicationAdminOrSameUser()]
        return super().get_permissions()
    
    def _validate_capacity_to_update_user_permission(self, serializer):
        request_user = self.request.user
        request_user_is_admin = request_user.permission and request_user.permission.is_admin

        if request_user_is_admin:
            return True
        
        serializer_user_permission = serializer.validated_data.get('user_permission', None)
        instance = self.get_object()
        instance_permission = instance.permission
        if not serializer_user_permission or (
            serializer_user_permission and instance_permission and
            serializer_user_permission.get('is_staff') == instance_permission.is_staff and
            serializer_user_permission.get('is_admin') == instance_permission.is_admin
        ):
            return True
        
        raise ValueError('Only admins are allowed to update user permissions')
    
    def perform_create(self, serializer):
        self._validate_capacity_to_update_user_permission(serializer)
        user = serializer.save()
        UserPermission.objects.create(user=user)

    def perform_update(self, serializer):
        self._validate_capacity_to_update_user_permission(serializer)
        user = serializer.save()
        UserPermission.objects.get_or_create(user=user)
