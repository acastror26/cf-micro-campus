from rest_framework.permissions import BasePermission

def _check_user_is_authenticated(user):
    return user and user.is_authenticated

class IsRequestingUser(BasePermission):
    """
    Custom permission to only allow requesting user to access the particular view.
    """
    def has_object_permission(self, request, view, obj):
        return _check_user_is_authenticated(request.user) and obj.requesting_user == request.user
    
class IsSameUser(BasePermission):
    """
    Custom permission to only allow the same user to access the particular view.
    """
    def has_object_permission(self, request, view, obj):
        return _check_user_is_authenticated(request.user) and obj == request.user

class IsApplicationStaff(BasePermission):
    """
    Custom permission to only allow staff users to access the view.
    """
    def has_permission(self, request, view):
        user = request.user
        if not _check_user_is_authenticated(user):
            return False
        permission = user.permission
        return permission and permission.is_staff
    
class IsApplicationAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        user = request.user
        if not _check_user_is_authenticated(user):
            return False
        permission = user.permission
        return permission and permission.is_admin
    
class IsApplicationAdminOrSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not _check_user_is_authenticated(user):
            return False
        permission = user.permission
        is_admin = permission and permission.is_admin
        is_same_user = obj == user
        return is_admin or is_same_user
    
class IsApplicationAdminOrRequestingUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not _check_user_is_authenticated(user):
            return False
        permission = user.permission
        is_admin = permission and permission.is_admin
        is_requesting_user = obj.requesting_user == user
        return is_admin or is_requesting_user
    
class IsApplicationStaffOrRequestingUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not _check_user_is_authenticated(user):
            return False
        permission = user.permission
        is_staff = permission and permission.is_staff
        is_requesting_user = obj.requesting_user == user
        return is_staff or is_requesting_user
    
class AllowGetForUnauthenticated(BasePermission):
    """
    Custom permission to allow GET requests for unauthenticated users
    and restrict other methods to authenticated users.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return _check_user_is_authenticated(request.user)