from django.contrib import admin
from .models import Room, ResourceType, Resource, Reservation, UserPermission
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.unregister(User)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'open_time', 'close_time')
    search_fields = ('id', 'name', 'address')
    fields = ('name', 'address', 'open_time', 'close_time')

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description')
    search_fields = ('id', 'type', 'description')
    fields = ('type', 'description')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'type', 'name', 'sku')
    list_filter = ('room', 'type')
    search_fields = ('sku', 'name', 'room__name', 'type__type')
    fields = ('room', 'type', 'name', 'sku')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'start_time', 'end_time', 'status', 'requesting_user', 'approver_user')
    list_filter = ('status',)
    search_fields = ('id', 'room__name', 'requesting_user__email', 'approver_user__email')

class UserPermissionInline(admin.StackedInline):
    model = UserPermission
    fields = ('is_staff', 'is_admin')
    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'get_is_staff', 'get_is_admin')
    search_fields = ('id', 'first_name', 'last_name', 'email')
    inlines = [UserPermissionInline]

    def get_is_staff(self, obj):
        return obj.permission.is_staff

    def get_is_admin(self, obj):
        return obj.permission.is_admin
    
    get_is_staff.short_description = 'Reservation Service Staff'
    get_is_admin.short_description = 'Reservation Service Admin'
    get_is_staff.admin_order_field = 'permission__is_staff'
    get_is_admin.admin_order_field = 'permission__is_admin'
