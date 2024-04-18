from django.db import models
from django.utils import timezone

class BenefitPlans(models.Model):
    BENEFIT_PLANS_ID = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    PLAN_NAME = models.CharField(max_length=10, null=True)
    DEDUCTABLE = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    PERCENTAGE_COPAY = models.DecimalField(max_digits=18, decimal_places=0, null=True)

    def __str__(self):
        return self.PLAN_NAME

    class Meta:
        ordering = ['BENEFIT_PLANS_ID']

class Employment(models.Model):
    EMPLOYMENT_ID = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    EMPLOYMENT_CODE = models.CharField(max_length=50, null=True)
    EMPLOYMENT_STATUS = models.CharField(max_length=10, null=True)
    HIRE_DATE_FOR_WORKING = models.DateField(default=timezone.now, null=True)  # Set default value to current date and time
    WORKERS_COMP_CODE = models.CharField(max_length=10, null=True, verbose_name='MÃ CÔNG VIỆC')
    TERMINATION_DATE = models.DateField(null=True)
    REHIRE_DATE_FOR_WORKING = models.DateField(null=True)
    LAST_REVIEW_DATE = models.DateField(null=True)
    NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    personal = models.ForeignKey('Personal', on_delete=models.CASCADE, null=True, related_name='employments')

    def __str__(self):
        return self.EMPLOYMENT_CODE if self.EMPLOYMENT_CODE else str(self.EMPLOYMENT_ID)

    class Meta:
        ordering = ['EMPLOYMENT_ID']

class EmploymentWorkingTime(models.Model):
    EMPLOYMENT_WORKING_TIME_ID = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    EMPLOYMENT = models.ForeignKey(Employment, on_delete=models.CASCADE, null=True, related_name='working_times')
    YEAR_WORKING = models.DateField(default=timezone.now, null=True)  # Set default value to current date and time
    MONTH_WORKING = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    NUMBER_DAYS_ACTUAL_OF_WORKING_PER_MONTH = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    TOTAL_NUMBER_VACATION_WORKING_DAYS_PER_MONTH = models.DecimalField(max_digits=2, decimal_places=0, null=True)

    def __str__(self):
        return str(self.EMPLOYMENT_WORKING_TIME_ID)

    class Meta:
        ordering = ['EMPLOYMENT_WORKING_TIME_ID']

class JobHistory(models.Model):
    JOB_HISTORY_ID = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    EMPLOYMENT = models.ForeignKey(Employment, on_delete=models.CASCADE, null=True, related_name='job_histories')
    DEPARTMENT = models.CharField(max_length=250, null=True)
    DIVISION = models.CharField(max_length=250, null=True)
    FROM_DATE = models.DateField(default=timezone.now, null=True)  # Set default value to current date and time
    THRU_DATE = models.DateField(null=True)
    JOB_TITLE = models.CharField(max_length=250, null=True)
    SUPERVISOR = models.CharField(max_length=250, null=True)
    LOCATION = models.CharField(max_length=250, null=True)
    TYPE_OF_WORK = models.SmallIntegerField(null=True)

    def __str__(self):
        return str(self.JOB_HISTORY_ID)

    class Meta:
        ordering = ['JOB_HISTORY_ID']

class Personal(models.Model):
    PERSONAL_ID = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    CURRENT_FIRST_NAME = models.CharField(max_length=50, null=True)
    CURRENT_LAST_NAME = models.CharField(max_length=50, null=True)
    CURRENT_MIDDLE_NAME = models.CharField(max_length=50, null=True)
    BIRTH_DATE = models.DateField(default=timezone.now, null=True)  # Set default value to current date and time
    SOCIAL_SECURITY_NUMBER = models.CharField(max_length=20, null=True)
    DRIVERS_LICENSE = models.CharField(max_length=50, null=True)
    CURRENT_ADDRESS_1 = models.CharField(max_length=255, null=True)
    CURRENT_ADDRESS_2 = models.CharField(max_length=255, null=True)
    CURRENT_CITY = models.CharField(max_length=100, null=True)
    CURRENT_COUNTRY = models.CharField(max_length=100, null=True)
    CURRENT_ZIP = models.DecimalField(max_digits=18, decimal_places=0, null=True)
    CURRENT_GENDER = models.CharField(max_length=20, null=True)
    CURRENT_PHONE_NUMBER = models.CharField(max_length=15, null=True)
    CURRENT_PERSONAL_EMAIL = models.CharField(max_length=50, null=True)
    CURRENT_MARITAL_STATUS = models.CharField(max_length=50, null=True)
    ETHNICITY = models.CharField(max_length=10, null=True)
    SHAREHOLDER_STATUS = models.SmallIntegerField(null=True)
    BENEFIT_PLAN = models.ForeignKey(BenefitPlans, on_delete=models.CASCADE, null=True, related_name='personals')

    def __str__(self):
        return f"{self.CURRENT_FIRST_NAME} {self.CURRENT_MIDDLE_NAME} {self.CURRENT_LAST_NAME}"

    class Meta:
        ordering = ['PERSONAL_ID']

class PayRate(models.Model):
    idPayRates = models.AutoField(primary_key=True)
    PayRateName = models.CharField(max_length=255)
    Value = models.DecimalField(max_digits=10, decimal_places=2)
    TaxPercentage = models.DecimalField(max_digits=5, decimal_places=2)
    PayType = models.IntegerField()
    PayAmount = models.DecimalField(max_digits=10, decimal_places=2)
    PTLevelC = models.DecimalField(max_digits=10, decimal_places=2)
    parent_payrate = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.PayRateName

    class Meta:
        ordering = ['idPayRates']

    def total_vacationday(self):
        # Lấy tổng số ngày nghỉ của mức lương
        total_vacation_days = 0
        for employee in self.employee_set.all():
            total_vacation_days += employee.total_vacation_days
        return total_vacation_days

class Employee(models.Model):
    idEmployee = models.AutoField(primary_key=True)
    EmployeeNumber = models.IntegerField(unique=True)
    LastName = models.CharField(max_length=255)
    FirstName = models.CharField(max_length=255)
    SSN = models.DecimalField(max_digits=9, decimal_places=0)
    PayRate = models.CharField(max_length=255, blank=True)
    PayRates_idPay = models.ForeignKey('PayRate', on_delete=models.CASCADE)  # Sử dụng 'PayRate' thay vì trường cụ thể
    VacationDays = models.IntegerField(null=True, blank=True)
    PaidToDate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PaidLastYear = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.LastName}, {self.FirstName}"

    class Meta:
        ordering = ['idEmployee']


    def total_payrate(self):
        return int(self.PayRates_idPay.PayAmount.to_integral_value())


    def total_vacationday(self):
        return self.VacationDays if self.VacationDays else 0