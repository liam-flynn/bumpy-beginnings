# help from https://www.coursera.org/learn/uol-cm3035-advanced-web-development/lecture/CgMEO/6-406-implement-a-chat-server

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Notifications, name='notifications'),
    path('<int:id>/', views.mark_as_read,
         name='mark_as_read')
]
