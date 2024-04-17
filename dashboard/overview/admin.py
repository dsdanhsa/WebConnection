from django.contrib import admin
from .models import PayRate, Employee, BenefitPlans, Personal, EmploymentWorkingTime, Employment, JobHistory

@admin.register(PayRate)
class PayRateAdmin(admin.ModelAdmin):
    list_display = ['idPayRates', 'PayRateName', 'Value', 'TaxPercentage', 'PayType', 'PayAmount', 'PTLevelC', 'parent_payrate']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['idEmployee', 'EmployeeNumber', 'LastName', 'FirstName', 'SSN', 'PayRate', 'VacationDays', 'PaidToDate']

@admin.register(BenefitPlans)
class BenefitPlansAdmin(admin.ModelAdmin):
    list_display = ['PLAN_NAME', 'DEDUCTABLE', 'PERCENTAGE_COPAY']

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ['PERSONAL_ID', 'CURRENT_FIRST_NAME', 'CURRENT_LAST_NAME', 'CURRENT_MIDDLE_NAME', 'CURRENT_ADDRESS_1', 'CURRENT_CITY', 'CURRENT_COUNTRY', 'CURRENT_ZIP', 'CURRENT_PERSONAL_EMAIL', 'CURRENT_PHONE_NUMBER', 'SOCIAL_SECURITY_NUMBER', 'DRIVERS_LICENSE', 'CURRENT_MARITAL_STATUS', 'CURRENT_GENDER', 'SHAREHOLDER_STATUS', 'BENEFIT_PLAN', 'ETHNICITY']

@admin.register(EmploymentWorkingTime)
class EmploymentWorkingTimeAdmin(admin.ModelAdmin):
    list_display = ['EMPLOYMENT_WORKING_TIME_ID', 'EMPLOYMENT', 'YEAR_WORKING', 'MONTH_WORKING', 'NUMBER_DAYS_ACTUAL_OF_WORKING_PER_MONTH', 'TOTAL_NUMBER_VACATION_WORKING_DAYS_PER_MONTH']

@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ['EMPLOYMENT_ID', 'EMPLOYMENT_CODE', 'EMPLOYMENT_STATUS', 'HIRE_DATE_FOR_WORKING', 'WORKERS_COMP_CODE', 'TERMINATION_DATE', 'REHIRE_DATE_FOR_WORKING', 'LAST_REVIEW_DATE', 'personal']

@admin.register(JobHistory)
class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ['JOB_HISTORY_ID', 'EMPLOYMENT', 'DEPARTMENT', 'DIVISION', 'FROM_DATE', 'THRU_DATE', 'JOB_TITLE', 'SUPERVISOR', 'LOCATION', 'TYPE_OF_WORK']

