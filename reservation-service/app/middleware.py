import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

User = get_user_model()

class BearerTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith('/api'):
            return
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logout(request)
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        token = auth_header.split(' ')[1]
        response = requests.post(
            'http://user-service:8000/token/validate',
            json={'access_token': token, 'token_type': 'Bearer'},
        )

        if response.status_code != 200:
            logout(request)
            return JsonResponse({'detail': 'Invalid token.'}, status=401)

        user_data = response.json()
        email = user_data.get('email')
        is_active = user_data.get('is_active')

        if not email or not is_active:
            logout(request)
            return JsonResponse({'detail': 'Invalid user data.'}, status=401)

        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        if created:
            user.set_unusable_password()
            user.save()

        login(request, user)