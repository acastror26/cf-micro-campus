from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .models import Room, ResourceType, Resource, Reservation, UserPermission
from .serializers import RoomSerializer, ResourceTypeSerializer, ResourceSerializer, ReservationSerializer, UserSerializer, LoginSerializer
from .permissions import IsApplicationStaff, IsApplicationAdminOrRequestingUser, IsApplicationAdmin, IsApplicationAdminOrSameUser, IsApplicationStaffOrRequestingUser, AllowGetForUnauthenticated
from .user_service import UserService, UserInfo
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

user_service = UserService()

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: 'Token response'}, operation_description='Login user in the user service and get token to use in the next requests')
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            if not email or not password:
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            token_response = user_service.generate_token(serializer.validated_data)
            print(token_response)
            return Response(token_response.dict(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowGetForUnauthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsApplicationAdmin()]
        return super().get_permissions() or []

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [AllowGetForUnauthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsApplicationAdmin()]
        return super().get_permissions() or []

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [AllowGetForUnauthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsApplicationStaff()]
        elif self.request.method == 'DELETE':
            return [IsApplicationAdmin()]
        return super().get_permissions() or []

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowGetForUnauthenticated]
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsApplicationAdminOrRequestingUser()]
        elif self.action == 'partial_update':
            return [IsApplicationStaffOrRequestingUser()]
        return super().get_permissions() or []

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
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
    queryset = User.objects.filter(permission__isnull=False)
    serializer_class = UserSerializer
    permission_classes = [AllowGetForUnauthenticated]

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsApplicationAdmin()]
        elif self.request.method in ['POST', 'PUT']:
            return [IsApplicationAdminOrSameUser()]
        return super().get_permissions() or []
    
    def _check_is_user_admin(self, user):
        print('is anonymous:', user.is_anonymous)
        return user.permission and user.permission.is_admin
    
    def _validate_capacity_to_update_user_permission(self, serializer):
        request_user = self.request.user
        request_user_is_admin = self._check_is_user_admin(request_user)

        if request_user_is_admin:
            return True
        
        is_staff = serializer.validated_data.get('is_staff', None)
        is_admin = serializer.validated_data.get('is_admin', None)
        instance = self.get_object()
        instance_permission = instance.permission
        if not instance:
            raise ValueError('Request user is invalid. Please contact an admin.')
        permission_changed = False
        if is_staff is not None and is_staff != instance_permission.is_staff:
            permission_changed = True
        if is_admin is not None and is_admin != instance_permission.is_admin:
            permission_changed = True

        if not permission_changed:
            return True
        
        raise ValueError('Only admins are allowed to update user permissions')

    def _confirm_reply_from_user_service(self, serializer, user_service_reply: UserInfo):
        if not user_service_reply:
            raise ValueError('Could not find user service reply')
        try:
            if serializer.validated_data.get('first_name', None):
                assert serializer.validated_data.get('first_name') == user_service_reply.first_name
            if serializer.validated_data.get('last_name', None):
                assert serializer.validated_data.get('last_name') == user_service_reply.last_name
            if serializer.validated_data.get('phone_number', None):
                assert serializer.validated_data.get('phone_number') == user_service_reply.phone_number
            if serializer.validated_data.get('country', None):
                assert serializer.validated_data.get('country') == user_service_reply.country
            if serializer.validated_data.get('state', None):
                assert serializer.validated_data.get('state') == user_service_reply.state
            if serializer.validated_data.get('city', None):
                assert serializer.validated_data.get('city') == user_service_reply.city
            serializer.validated_data['user_service_id'] = user_service_reply.id
        except AssertionError:
            raise ValueError('User service reply does not match the user data')
        return serializer
    
    def _get_user_service_id(self, instance):
        if not instance.permission or not instance.permission.user_service_id:
            raise ValueError('User does not have user service id')
        return instance.permission.user_service_id
    
    def perform_create(self, serializer):
        print('reached view!!')
        self._validate_capacity_to_update_user_permission(serializer)
        user_service_reply: UserInfo = user_service.create_user(serializer.validated_data, request=self.request)
        serializer = self._confirm_reply_from_user_service(serializer, user_service_reply)
        user = serializer.save()

    def perform_update(self, serializer):
        self._validate_capacity_to_update_user_permission(serializer)
        user_service_id = self._get_user_service_id(serializer.instance)
        user_service_reply: UserInfo = user_service.update_user(user_service_id, serializer.validated_data)
        serializer = self._confirm_reply_from_user_service(serializer, user_service_reply)
        serializer.validated_data['email'] = serializer.instance.email
        print('validated data:', serializer.validated_data)
        user = serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user or not self._check_is_user_admin(self.request.user):
            raise ValueError('Only admins are allowed to delete users')
        if self.request.user == instance:
            raise ValueError('Cannot delete self')
        user_service_id = self._get_user_service_id(instance)
        user_service_reply: int = user_service.delete_user(user_service_id)
        print('user service reply:', user_service_reply)
        if not user_service_reply or user_service_id != user_service_reply:
            raise ValueError('Could not delete user from user service')
        instance.delete()