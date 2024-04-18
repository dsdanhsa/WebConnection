from django.urls import path
from . import views

app_name = 'hrapp'

urlpatterns = [
    path('benefitplans/', views.Benefitplans_list, name='benefitplans'),
    path('employmentworkingtime/', views.EmploymentWorkingTime_list, name='employmentworkingtime'),
    path('employment/', views.Employment_list, name='employment'),
    path('jobhistory/', views.Jobhistory_lisst, name='jobhistory'),
    path('personal/', views.Personal_list, name='personal')
]