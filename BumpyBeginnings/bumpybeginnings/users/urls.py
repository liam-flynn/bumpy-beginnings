from django.urls import include, path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('get-details/', views.get_details, name='get_details'),
    path('logout/', views.user_logout, name='logout'),
    path('update-profile/', views.profile_update, name='profile_update'),
    path('manage-mod-privileges/', views.manage_mod_privileges,
         name='manage_mod_privileges'),
    path('cms/', views.cms_dashboard, name='cms-dashboard'),
    path('', views.homepage, name='homepage'),
]
