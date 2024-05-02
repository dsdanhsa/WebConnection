from django.urls import path
from .views import totalpayrate, totalvacation, birthday_count, benefitplan, excessvacationday, changebenefit_detail, changebenefit_update, changeemployee_detail, employee_update, employment_update, personal_update, employee_add

app_name = 'overview_app'

urlpatterns = [
    path('', totalpayrate, name='totalpayrate'),
    path('totalvacation/', totalvacation, name='totalvacation'),
    path('birthday_count/', birthday_count, name='birthday_count'),
    path('benefitplan/', benefitplan, name='benefitplan'),
    path('excess/', excessvacationday, name='excessvacationday'),
    path('benefit_detail/', changebenefit_detail, name='benefit_detail'),
    path('benefit_update/<int:benefitid>/', changebenefit_update, name='benefit_update'),

    #cập nhật của bảng HR và Payroll
    path('employee_detail/', changeemployee_detail, name='employee_detail'),
    path('employee_update/<int:employeeid>/', employee_update, name='employee_update'),
    path('employment_update/<int:employmentid>/', employment_update, name='employment_update'),
    path('personal_update/<int:personalid>/', personal_update, name='personal_update'),

    #add HR và payroll
    path('employee_add/', employee_add, name='employee_add'),
]
