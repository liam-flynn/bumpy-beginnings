from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.questionnaire, name='questionnaire'),
    path('benefit-list/', views.manage_benefits_list, name='benefit_list'),

    path("benefit/create/", views.create_benefit, name="create_benefit"),
    path('benefit/edit/<int:benefit_id>/',
         views.edit_benefit, name='edit_benefit'),
    path('benefit/delete/<int:benefit_id>/',
         views.delete_benefit, name='delete_benefit'),

    path("benefit-rate/create/", views.create_benefit_rate,
         name="create_benefit_rate"),
    path('benefit-rate/edit/<int:rate_id>/',
         views.edit_benefit_rate, name='edit_benefit_rate'),
    path('benefit-rate/delete/<int:rate_id>/',
         views.delete_benefit_rate, name='delete_benefit_rate'),

    path("criteria/create/", views.create_eligibility_criteria,
         name="create_eligibility_criteria"),
    path('criteria/edit/<int:criteria_id>/',
         views.edit_eligibility_criteria, name='edit_eligibility_criteria'),
    path('criteria/delete/<int:criteria_id>/',
         views.delete_eligibility_criteria, name='delete_eligibility_criteria'),
]
