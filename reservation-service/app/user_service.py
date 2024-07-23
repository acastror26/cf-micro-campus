from django.conf import settings
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .serializers import UserSerializer
from pydantic import BaseModel  
from typing import Optional
from django.middleware.csrf import get_token as get_csrf_token
from django.core.cache import cache

class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = False

class UserInfo(UserBase):    
    email: str
    id: int

class UserCreate(UserInfo):
    email: str
    password: str

class TokenValidate(BaseModel):
    user: UserInfo
    is_valid: bool

class TokenGenerate(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class UserService:
    def __init__(self) -> None:
        self.initialized = False
        self.url = None
        self.session = None
        if settings.USER_SERVICE_URL is not None and settings.USER_SERVICE_URL != '':
            self.initialized = True
            self.url = settings.USER_SERVICE_URL
            session = requests.Session()
            retry = Retry(connect=1, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            self.session = session
    
    def _check_initialized(self):
        if not self.initialized:
            raise Exception('User service not initialized')
        
    def _get_client_authentication_token(self):
        key = 'client_authentication_token'
        access_token = cache.get(key)
        if not access_token:
            if not settings.CLIENT_ID or not settings.CLIENT_SECRET:
                raise Exception('Client ID and Client Secret not set in settings')
            data = {
                'email': settings.CLIENT_ID,
                'password': settings.CLIENT_SECRET
            }
            token: TokenGenerate = self.generate_token(data)
            cache.set(key, token.access_token, token.expires_in)
            access_token = token.access_token
        return access_token
        
    def _get_headers(self, url: str, request=None):
        headers = {}
        if request:
            csrf_token = get_csrf_token(request)
            headers['X-CSRFToken'] = csrf_token
        if 'users' in url:  # only add authentication for user endpoints
            access_token = self._get_client_authentication_token()
            headers['Authorization'] = f'Bearer {access_token}'
        return headers
    
    def _do_request(self, method: str, url: str, data: dict = {}, expected_code=200, request=None):
        print('making request...')
        headers = self._get_headers(request=request, url=url)
        print(headers)
        response = self.session.request(method, url, json=data, headers=headers)
        print(response.text)
        if response.status_code != expected_code:
            raise Exception('Failed request to user service. Error: ' + response.text)
        
        return response
        
    def update_user(self, user_id: int, data: dict, request=None) -> dict:
        self._check_initialized()
        url = f'{self.url}/users/{user_id}'
        response = self._do_request('PUT', url, data, request=request)

        return UserInfo(**response.json())
    
    def create_user(self, data: dict, request=None) -> dict:
        self._check_initialized()
        url = f'{self.url}/users/'
        response = self._do_request('POST', url, data, request=request)

        return UserInfo(**response.json())
    
    def delete_user(self, user_id: int) -> None:
        self._check_initialized()
        url = f'{self.url}/users/{user_id}'
        response = self._do_request('DELETE', url)
        print(response)

        return user_id
    
    def validate_token(self, token: str, request=None):
        self._check_initialized()
        url = f'{self.url}/token/validate'
        data = {'access_token': token, 'token_type': 'Bearer'}
        response = self._do_request('POST', url, data, request=None)
        print(response)
        return TokenValidate(**response.json())
    
    def generate_token(self, data: dict):
        self._check_initialized()
        url = f'{self.url}/token/'
        response = self._do_request('POST', url, data)
        print(response)
        return TokenGenerate(**response.json())
