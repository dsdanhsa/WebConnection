from django.shortcuts import render
from payroll_app.models import PayRate, Employee
from django.contrib.auth.decorators import login_required
from hrapp.models import BenefitPlans, Employment, EmploymentWorkingTime, JobHistory, Personal
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import base64


@login_required
def totalpayrate(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count = calculate_totals()

    # Tạo biểu đồ Pay Amount by Employee Number
    plt.bar(categories, pay_values)
    plt.xlabel('Employee Number')
    plt.ylabel('Pay Amount')
    plt.title('Pay Amount by Employee Number')
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.getvalue()).decode()
    plt.close()

    content = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'chart_data': img_base64,
        'birthday_count': birthday_count
    }

    return render(request, 'overview_app/home.html', content)

@login_required
def totalvacation(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count = calculate_totals()

    # Tạo biểu đồ Vacation Days by Employee Number
    plt.bar(categories, vacation_values)
    plt.xlabel('Employee Number')
    plt.ylabel('Vacation Days')
    plt.title('Vacation Days by Employee Number')
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.getvalue()).decode()
    plt.close()

    context = {
        'chart_data': img_base64,
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count
    }

    return render(request, 'overview_app/overview_vacation.html', context)

@login_required
def birthday_count(request):
    current_month = datetime.now().month
    birthdays = Personal.objects.filter(BIRTH_DATE__month=current_month)
    birthday_count = birthdays.count()

    birthday_list = birthdays.values_list('CURRENT_FIRST_NAME', 'CURRENT_MIDDLE_NAME', 'CURRENT_LAST_NAME', 'BIRTH_DATE', 'CURRENT_ADDRESS_1', 'CURRENT_PHONE_NUMBER')

    return render(request, 'overview_app/birthday.html',
                  {'birthday_count': birthday_count, 'birthday_list': birthday_list})

def calculate_totals():
    Employees = Employee.objects.all()
    totalpayrate = 0
    totalvacationday = 0
    categories = []
    pay_values = []
    vacation_values = []

    current_month = datetime.now().month
    birthdays = Personal.objects.filter(BIRTH_DATE__month=current_month)
    birthday_count = birthdays.count()

    for employee in Employees:
        totalpayrate += employee.total_payrate()
        totalvacationday += employee.total_vacationday()
        categories.append(employee.EmployeeNumber)
        pay_values.append(employee.PayRates_idPay.PayAmount)
        vacation_values.append(employee.VacationDays)

    return totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count