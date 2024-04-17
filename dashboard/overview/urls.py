from django.urls import path
from . import views

app_name = 'overview'

urlpatterns = [
    path('', views.payroll_overview, name='overview'),
]