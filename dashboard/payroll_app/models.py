from django.db import models

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

    def __str__(self):
        return f"{self.LastName}, {self.FirstName}"

    class Meta:
        ordering = ['idEmployee']


    def total_payrate(self):
        return int(self.PayRates_idPay.PayAmount.to_integral_value())


    def total_vacationday(self):
        return self.VacationDays if self.VacationDays else 0