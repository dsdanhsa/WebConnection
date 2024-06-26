from django.urls import path
from .views import totalpayrate, totalvacation, birthday_count, benefitplan, excessvacationday, changebenefit_detail, changebenefit_update, changeemployee_detail, employee_update, employment_update, personal_update, employee_add, personal_add, employment_add, employee_delete,tbtotalpayrate, hiringanniversary, hiringngay304,hiringngay75,hiringthanhlapcongty, hiringlamviectren3nam

app_name = 'overview_app'

urlpatterns = [
    #home
    path('', totalpayrate, name='totalpayrate'),
    path('tbtotalpayrate/', tbtotalpayrate, name='tbtotalpayrate'),
    path('totalvacation/', totalvacation, name='totalvacation'),
    path('birthday_count/', birthday_count, name='birthday_count'),
    path('benefitplan/', benefitplan, name='benefitplan'),
    path('excess/', excessvacationday, name='excessvacationday'),
    path('hiringanniversary/', hiringanniversary, name='hiringanniversary'),
    path('benefit_detail/', changebenefit_detail, name='benefit_detail'),
    path('benefit_update/<int:benefitid>/', changebenefit_update, name='benefit_update'),


    #tb hiring các sự kiện quan trọng
    path('hiringngay304/', hiringngay304, name='hiringngay304'),
    path('hiringngay75/', hiringngay75, name='hiringngay75'),
    path('hiringthanhlapcongty/', hiringthanhlapcongty, name='hiringthanhlapcongty'),
    path('hiringlamviectren3nam/', hiringlamviectren3nam, name='hiringlamviectren3nam'),

    #cập nhật của bảng HR và Payroll
    path('employee_detail/', changeemployee_detail, name='employee_detail'),
    path('employee_update/<int:employeeid>/', employee_update, name='employee_update'),
    path('employment_update/<int:employmentid>/', employment_update, name='employment_update'),
    path('personal_update/<int:personalid>/', personal_update, name='personal_update'),

    #add HR và payroll
    path('employee_add/', employee_add, name='employee_add'),
    path('personal_add/', personal_add, name='personal_add'),
    path('employment_add/', employment_add, name='employment_add'),

    #Xóa HR và Payroll
    path('employee_delete/', employee_delete, name='employee_delete'),
]
