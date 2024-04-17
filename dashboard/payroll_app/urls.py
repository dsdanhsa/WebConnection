from django.urls import path
from . import views

app_name = 'payroll_app'

urlpatterns = [
    path('list_payrate/', views.payrate_list, name='payrate_list'),
    path('list_employee/', views.employee_list, name='employee_list'),
]