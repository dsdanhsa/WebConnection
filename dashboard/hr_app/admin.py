from django.contrib import admin
from .models import MigrationHistory, Benefit_Plans, Personal, Emergency_Contacts, Employment, Job_History

@admin.register(MigrationHistory)
class MigrationHistoryAdmin(admin.ModelAdmin):
    list_display = ['MigrationId', 'ContextKey', 'ProductVersion']

@admin.register(Benefit_Plans)
class BenefitPlansAdmin(admin.ModelAdmin):
    list_display = ['Plan_Name', 'Deductable', 'Percentage_CoPay']

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ['Employee_ID', 'First_Name', 'Last_Name', 'Middle_Initial', 'Address1', 'City', 'State', 'Zip', 'Email', 'Phone_Number', 'Social_Security_Number', 'Drivers_License', 'Marital_Status', 'Gender', 'Shareholder_Status', 'Benefit_Plans', 'Ethnicity']

@admin.register(Emergency_Contacts)
class EmergencyContactsAdmin(admin.ModelAdmin):
    list_display = ['Emergency_Contact_Name', 'Phone_Number', 'Relationship', 'employee_id']

@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ['employment_employee_id', 'Employment_Status', 'Hire_Date', 'Workers_Comp_Code', 'Termination_Date', 'Rehire_Date', 'Last_Review_Date', 'personal']

@admin.register(Job_History)
class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ['job_employee_id', 'Department', 'Division', 'Start_Date', 'End_Date', 'Job_Title', 'Supervisor', 'Job_Category', 'Location', 'Departmen_Code', 'Salary_Type', 'Pay_Period', 'Hours_per_Week', 'Hazardous_Training']
