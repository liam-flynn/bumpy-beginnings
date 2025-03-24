from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isMother = models.BooleanField(default=True)
    dueDate = models.DateField(null=False)
    partnerName = models.CharField(max_length=80, blank=True,validators=[RegexValidator(regex=r'^[^\0]*$', message="Null characters are not allowed.")]
    )
    isForumMod = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    