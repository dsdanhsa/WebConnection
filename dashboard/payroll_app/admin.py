from django.contrib import admin
from .models import PayRate, Employee

@admin.register(PayRate)
class PayRateAdmin(admin.ModelAdmin):
    list_display = ['idPayRates', 'PayRateName', 'Value', 'TaxPercentage', 'PayType', 'PayAmount', 'PTLevelC', 'parent_payrate']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['idEmployee', 'EmployeeNumber', 'LastName', 'FirstName', 'SSN', 'PayRate', 'VacationDays', 'PaidToDate', 'PaidLastYear']
