
from datetime import datetime, timezone

from django.db import models
from django.contrib.auth.models import User

def add_timezone_to_datetime(dt, tz=timezone.utc):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt

class UserPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permission')
    user_data = models.JSONField(default={})
    user_service_id = models.IntegerField(null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if self.is_admin and not self.is_staff:
            self.is_staff = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    open_time = models.DateTimeField(null=True, blank=True)
    close_time = models.DateTimeField(null=True, blank=True)

    @property
    def display_name(self):
        return str(self)
    
    def __str__(self):
        return self.name or 'Room ' + str(self.id)

class ResourceType(models.Model):
    type = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.type

class Resource(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)

    def __str__(self):
        return self.sku

class Reservation(models.Model):
    APPROVED = 'APPROVED'
    DENIED = 'DENIED'
    REVIEW_PENDING = 'REVIEW_PENDING'
    
    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (DENIED, 'Denied'),
        (REVIEW_PENDING, 'Review Pending'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REVIEW_PENDING)
    requesting_user = models.ForeignKey(User, related_name='requesting_user', on_delete=models.SET_NULL, null=True, blank=False)
    requesting_user_information_metadata = models.JSONField(blank=True, null=True)
    approver_user = models.ForeignKey(User, related_name='approver_user', on_delete=models.SET_NULL, null=True, blank=True)
    approver_user_information_metadata = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if self.start_time > self.end_time:
            raise ValueError('Start time must be before end time')
        if self.start_time == self.end_time:
            raise ValueError('Start time and end time cannot be the same')
        if self.room.open_time and self.start_time < self.room.open_time:
            raise ValueError('Start time must be after room open time')
        if self.room.close_time and self.end_time > self.room.close_time:
            raise ValueError('End time must be before room close time')
        if self.start_time < add_timezone_to_datetime(datetime.now()):
            raise ValueError('Start time must be in the future')
        if self.requesting_user and self.approver_user and self.requesting_user == self.approver_user:
            raise ValueError('Requesting user and approver user cannot be the same')
        if self.requesting_user and self.requesting_user_information_metadata is None:
            self.requesting_user_information_metadata = {
                'id': self.requesting_user.id,
                'email': self.requesting_user.email,
            }
        if self.approver_user and self.approver_user_information_metadata is None:
            self.approver_user_information_metadata = {
                'id': self.approver_user.id,
                'email': self.approver_user.email,
            }
        return super().save(*args, **kwargs)
