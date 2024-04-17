from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PayRate, Employee

@login_required
def payroll_overview(request):
    Employees = Employee.objects.all()
    totalpayrate = 0
    totalvacationday = 0
    for i in Employees:
        totalpayrate += i.total_payrate()
    for i in Employees:
        totalvacationday += i.total_vacationday()
    content = {'Employees': Employees, 'totalpayrate':totalpayrate, 'totalvacationday': totalvacationday}
    return render(request, 'overview/home.html',content)