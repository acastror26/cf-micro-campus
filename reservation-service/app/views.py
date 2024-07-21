from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Room, ResourceType, Resource, Reservation
from .serializers import RoomSerializer, ResourceTypeSerializer, ResourceSerializer, ReservationSerializer, UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super(RoomViewSet, self).get_permissions()

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [IsAuthenticated]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            self.permission_classes = [IsAdminUser | IsStaff]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAdminUser]
        return super(ResourceViewSet, self).get_permissions()

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(requesting_user=user)

    def perform_create(self, serializer):
        serializer.save(requesting_user=self.request.user, approver_user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save(approver_user=self.request.user)
        serializer.save()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super(UserViewSet, self).get_permissions()
