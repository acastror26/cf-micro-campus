from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

    def __str__(self):
        return self.name or 'Room ' + str(self.id)

class ResourceType(models.Model):
    type = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.type

class Resource(models.Model):
    SKU = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.SKU

class Reservation(models.Model):
    APPROVED = 'APPROVED'
    DENIED = 'DENIED'
    REVIEW_PENDING = 'REVIEW_PENDING'
    
    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (DENIED, 'Denied'),
        (REVIEW_PENDING, 'Review Pending'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REVIEW_PENDING)
    requesting_user = models.ForeignKey(User, related_name='requesting_user', on_delete=models.CASCADE)
    approver_user = models.ForeignKey(User, related_name='approver_user', on_delete=models.CASCADE)
