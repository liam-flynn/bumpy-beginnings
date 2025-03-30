from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SiteUser


class SiteUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SiteUser
        fields = ['id', 'user', 'isMother',
                  'dueDate', 'partnerName', 'isForumMod']
