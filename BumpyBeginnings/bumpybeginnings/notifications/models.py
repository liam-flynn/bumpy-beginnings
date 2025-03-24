from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# code based upon my AWD Final project with alterations
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} : {self.message}"

    def mark_as_read(self):
        self.is_read = True
        self.save()