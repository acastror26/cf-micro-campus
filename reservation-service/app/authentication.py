import requests
from typing import Any
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from app.models import UserPermission
from .user_service import UserService, TokenValidate, UserInfo
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()
user_service = UserService()

def _update_user_information(user, user_information: UserInfo):
    first_name = user_information.first_name
    last_name = user_information.last_name
    is_active = user_information.is_active
    user_updated = False
    if first_name is not None and user.first_name != first_name:
        user.first_name = first_name
        user_updated = True
    if last_name is not None and user.last_name != last_name:
        user.last_name = last_name
        user_updated = True
    if is_active is not None and user.is_active != is_active:
        user.is_active = is_active
        user_updated = True
    if user_updated:
        user.save()

    user_data = user_information.dict(exclude={'first_name', 'last_name', 'is_active', 'id', 'email'})
    
    # Update permission and user data
    permission, _ = UserPermission.objects.get_or_create(user=user, user_service_id=user_information.id)
    permission_updated = False
    if user_data != {} and permission.user_data != user_data:
        permission.user_data = user_data
        permission_updated = True
    if permission_updated:
        permission.save()
    return user
    

class BearerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authentication credentials were not provided.')

        token = auth_header.split(' ')[1]
        try:
            response: TokenValidate = user_service.validate_token(token)
        except Exception as e:
            raise AuthenticationFailed(f'User service Response error: {str(e)}')

        user_information: UserInfo = response.user
        is_valid = response.is_valid
        email = user_information.email
        user_service_id = user_information.id

        if not user_information or not is_valid or not email or not user_service_id:
            raise AuthenticationFailed('Invalid user data from user service.')

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed('User not found in reservation service.')
        
        user = _update_user_information(user, user_information)
        print('User found:', user)
        return (user, None)
