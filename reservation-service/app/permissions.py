from rest_framework.permissions import BasePermission

class IsRequestingUser(BasePermission):
    """
    Custom permission to only allow requesting user to access the particular view.
    """
    def has_object_permission(self, request, view, obj):
        return obj.requesting_user == request.user
    
class IsSameUser(BasePermission):
    """
    Custom permission to only allow the same user to access the particular view.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsApplicationStaff(BasePermission):
    """
    Custom permission to only allow staff users to access the view.
    """
    def has_permission(self, request, view):
        user = request.user
        permission = user.permission
        return user and permission and permission.is_staff
    
class IsApplicationAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        user = request.user
        permission = user.permission
        return user and permission and permission.is_admin
    
class IsApplicationAdminOrSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = user.permission
        is_admin = permission and permission.is_admin
        is_same_user = obj == user
        return is_admin or is_same_user
    
class IsApplicationAdminOrRequestingUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = user.permission
        is_admin = permission and permission.is_admin
        is_requesting_user = obj.requesting_user == user
        return is_admin or is_requesting_user
    
class IsApplicationStaffOrRequestingUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = user.permission
        is_staff = permission and permission.is_staff
        is_requesting_user = obj.requesting_user == user
        return is_staff or is_requesting_user