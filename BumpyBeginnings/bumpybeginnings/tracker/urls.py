from django.urls import include, path
from . import views
from .views import DevelopmentMilstoneListView


urlpatterns = [
      path('new/', views.create_milestone, name='create_milestone'),
      path('<int:id>/delete/', views.delete_milestone, name='delete_milestone'),
      path('<int:id>/edit/', views.edit_milestone, name='edit_milestone'),
      path('<int:id>/view/', views.view_milestone, name='view_milestone'),
      path('user-milestone', views.get_current_milestone, name='user_milestone'),
      path('', DevelopmentMilstoneListView.as_view(), name='trackers'),
    ]