from django.shortcuts import render, get_object_or_404, redirect
from payroll_app.models import PayRate, Employee
from django.contrib.auth.decorators import login_required
from hrapp.models import BenefitPlans, Employment, EmploymentWorkingTime, JobHistory, Personal
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import base64

#tổng tiền lương và vẽ biểu đồ
@login_required
def totalpayrate(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()

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
        'birthday_count': birthday_count,
        'totalexcess' : totalexcess
    }

    return render(request, 'overview_app/home.html', content)

#tổng ngày nghĩ và vẽ biểu đồ
@login_required
def totalvacation(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()

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
        'birthday_count': birthday_count,
        'totalexcess' : totalexcess
    }

    return render(request, 'overview_app/overview_vacation.html', context)

#tính tổng người sn trong tháng này và list ra
@login_required
def birthday_count(request):
    current_month = datetime.now().month
    birthdays = Personal.objects.filter(BIRTH_DATE__month=current_month)
    birthday_count = birthdays.count()

    birthday_list = birthdays.values_list('CURRENT_FIRST_NAME', 'CURRENT_MIDDLE_NAME', 'CURRENT_LAST_NAME', 'BIRTH_DATE', 'CURRENT_ADDRESS_1', 'CURRENT_PHONE_NUMBER')

    return render(request, 'overview_app/birthday.html',
                  {'birthday_count': birthday_count, 'birthday_list': birthday_list})

#hàm thông báo về benefit
@login_required
def benefitplan(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    benefits = BenefitPlans.objects.all()
    context = {
        'benefits': benefits,
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess' : totalexcess
    }
    return render(request, 'overview_app/benefitplan.html', context)

#hàm tính tổng ngày ngĩ và liệt kê từng người nghĩ
@login_required
def excessvacationday(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    excess = []
    Employees = Employee.objects.all()
    for employee in Employees:
        if employee.VacationDays > 2:
            excess.append(employee)
    context = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess,
        'excess': excess
    }
    return render(request, 'overview_app/excessvacationday.html', context)

#change benefit
@login_required
def changebenefit_detail(request):
    changebenefits = BenefitPlans.objects.all()
    context = {'changebenefits': changebenefits}
    return render(request, 'overview_app/changebenefit_detail.html', context)

@login_required
def changebenefit_update(request, benefitid):
    changebenefits = get_object_or_404(BenefitPlans, BENEFIT_PLANS_ID=benefitid)
    if request.method == 'POST':
        planname = request.POST.get('planname')
        deductable = request.POST.get('deductable')
        percentage_copay = request.POST.get('percentage_copay')

        changebenefits.PLAN_NAME = planname
        changebenefits.DEDUCTABLE = deductable
        changebenefits.PERCENTAGE_COPAY = percentage_copay
        changebenefits.save()
        return redirect('benefit_detail')
    return render(request, 'overview_app/changebenefit_update.html', {'changebenefits': changebenefits})


#hàm chung xuất ra các giá trị trong code
def calculate_totals():
    Employees = Employee.objects.all()
    totalpayrate = 0
    totalvacationday = 0
    totalexcess = 0
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
        if employee.VacationDays > 2:
            totalexcess += 1
    return totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess

#thay doi thong tin ở HR và Payroll
@login_required
def changeemployee_detail(request):
    employees = Employee.objects.all()
    employments = Employment.objects.all()
    personals = Personal.objects.all()
    employee_data = zip(employees, employments, personals)
    context = {'employee_data':employee_data}
    return render(request, 'overview_app/changeemployee_detail.html', context)

#update employee
@login_required
def employee_update(request, employeeid):
    employee = get_object_or_404(Employee, idEmployee=employeeid)

    if request.method == "POST":
        rq_employee_number = request.POST.get("employee_number")
        rq_last_name = request.POST.get("last_name")
        rq_first_name = request.POST.get("first_name")
        rq_ssn = request.POST.get("ssn")
        rq_pay_rate = request.POST.get("pay_rate")
        rq_vacation_days = request.POST.get("vacation_days")
        rq_paid_to_date = request.POST.get("paid_to_date")
        rq_paid_last_year = request.POST.get("paid_last_year")

        employee.EmployeeNumber = rq_employee_number
        employee.LastName = rq_last_name
        employee.FirstName = rq_first_name
        employee.SSN = rq_ssn
        employee.PayRate = rq_pay_rate
        employee.VacationDays = rq_vacation_days
        employee.PaidToDate = rq_paid_to_date
        employee.PaidLastYear = rq_paid_last_year

        employee.save()

        list_employee = Employee.objects.all()
        context = {'list_employee': list_employee}
        return render(request, "overview_app/changeemployee_detail.html", context)
    else:
        context = {'employee': employee}
        return render(request, 'overview_app/changeemployee_update.html', context)

#update employment
@login_required
def employment_update(request, employmentid):
    employment = get_object_or_404(Employment, EMPLOYMENT_ID=employmentid)

    if request.method == "POST":
        rq_employment_code = request.POST.get("employment_code")
        rq_employment_status = request.POST.get("employment_status")
        rq_hire_date_for_working = request.POST.get("hire_date_for_working")
        rq_workers_comp_code = request.POST.get("workers_comp_code")
        rq_termination_date = request.POST.get("termination_date")
        rq_rehire_date_for_working = request.POST.get("rehire_date_for_working")
        rq_last_review_date = request.POST.get("last_review_date")
        rq_number_days_requirement_of_working_per_month = request.POST.get("number_days_requirement_of_working_per_month")

        employment.EMPLOYMENT_CODE = rq_employment_code
        employment.EMPLOYMENT_STATUS = rq_employment_status
        employment.HIRE_DATE_FOR_WORKING = rq_hire_date_for_working
        employment.WORKERS_COMP_CODE = rq_workers_comp_code
        employment.TERMINATION_DATE = rq_termination_date
        employment.REHIRE_DATE_FOR_WORKING = rq_rehire_date_for_working
        employment.LAST_REVIEW_DATE = rq_last_review_date
        employment.NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH = rq_number_days_requirement_of_working_per_month

        employment.save()

        return render(request, "overview_app/changeemployee_detail.html")
    else:
        context = {'employment': employment}
        return render(request, 'overview_app/employment_update.html', context)

#update personal
@login_required
def personal_update(request, personalid):
    personal = get_object_or_404(Personal, PERSONAL_ID=personalid)

    if request.method == "POST":
        rq_current_first_name = request.POST.get("current_first_name")
        rq_current_last_name = request.POST.get("current_last_name")
        rq_current_middle_name = request.POST.get("current_middle_name")
        rq_birth_date = request.POST.get("birth_date")
        rq_social_security_number = request.POST.get("social_security_number")
        rq_drivers_license = request.POST.get("drivers_license")
        rq_current_address_1 = request.POST.get("current_address_1")
        rq_current_address_2 = request.POST.get("current_address_2")
        rq_current_city = request.POST.get("current_city")
        rq_current_country = request.POST.get("current_country")
        rq_current_zip = request.POST.get("current_zip")
        rq_current_gender = request.POST.get("current_gender")
        rq_current_phone_number = request.POST.get("current_phone_number")
        rq_current_personal_email = request.POST.get("current_personal_email")
        rq_current_marital_status = request.POST.get("current_marital_status")
        rq_ethnicity = request.POST.get("ethnicity")
        rq_shareholder_status = request.POST.get("shareholder_status")
        rq_benefit_plan_id = request.POST.get("benefit_plan")

        # Cập nhật thông tin cá nhân
        personal.CURRENT_FIRST_NAME = rq_current_first_name
        personal.CURRENT_LAST_NAME = rq_current_last_name
        personal.CURRENT_MIDDLE_NAME = rq_current_middle_name
        personal.BIRTH_DATE = rq_birth_date
        personal.SOCIAL_SECURITY_NUMBER = rq_social_security_number
        personal.DRIVERS_LICENSE = rq_drivers_license
        personal.CURRENT_ADDRESS_1 = rq_current_address_1
        personal.CURRENT_ADDRESS_2 = rq_current_address_2
        personal.CURRENT_CITY = rq_current_city
        personal.CURRENT_COUNTRY = rq_current_country
        personal.CURRENT_ZIP = rq_current_zip
        personal.CURRENT_GENDER = rq_current_gender
        personal.CURRENT_PHONE_NUMBER = rq_current_phone_number
        personal.CURRENT_PERSONAL_EMAIL = rq_current_personal_email
        personal.CURRENT_MARITAL_STATUS = rq_current_marital_status
        personal.ETHNICITY = rq_ethnicity
        personal.SHAREHOLDER_STATUS = rq_shareholder_status
        personal.BENEFIT_PLAN = BenefitPlans.objects.get(BENEFIT_PLANS_ID=rq_benefit_plan_id)

        personal.save()

        return render(request, "overview_app/changeemployee_detail.html")
    else:
        benefit_plans = BenefitPlans.objects.all()
        context = {'personal': personal, 'benefit_plans': benefit_plans}
        return render(request, 'overview_app/personal_update.html', context)

#add emplployee
@login_required
def employee_add(request):
    if request.method == "POST":

        #add employee
        rq_employee_number = request.POST.get("employee_number")
        rq_last_name = request.POST.get("last_name")
        rq_first_name = request.POST.get("first_name")
        rq_ssn = request.POST.get("ssn")
        rq_pay_rate = request.POST.get("pay_rate")
        rq_vacation_days = request.POST.get("vacation_days")
        rq_paid_to_date = request.POST.get("paid_to_date")
        rq_paid_last_year = request.POST.get("paid_last_year")
        data = Employee(EmployeeNumber = rq_employee_number, LastName = rq_last_name,FirstName = rq_first_name,SSN = rq_ssn, PayRate = rq_pay_rate,
                        VacationDays = rq_vacation_days, PaidToDate = rq_paid_to_date, PaidLastYear = rq_paid_last_year)
        data.save()

        #add employment
        rq_employment_code = request.POST.get("employee_number")
        rq_employment_status = request.POST.get("employment_status")
        rq_hire_date_for_working = request.POST.get("hire_date_for_working")
        rq_workers_comp_code = request.POST.get("workers_comp_code")
        rq_termination_date = request.POST.get("termination_date")
        rq_rehire_date_for_working = request.POST.get("rehire_date_for_working")
        rq_last_review_date = request.POST.get("last_review_date")
        rq_number_days_requirement_of_working_per_month = request.POST.get("number_days_requirement_of_working_per_month")
        datahr1 = Employment(EMPLOYMENT_CODE = rq_employment_code, EMPLOYMENT_STATUS = rq_employment_status, HIRE_DATE_FOR_WORKING = rq_hire_date_for_working,
                             WORKERS_COMP_CODE = rq_workers_comp_code, TERMINATION_DATE = rq_termination_date, REHIRE_DATE_FOR_WORKING = rq_rehire_date_for_working,
                             LAST_REVIEW_DATE = rq_last_review_date, NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH = rq_number_days_requirement_of_working_per_month)
        datahr1.save()

        #add peronal
        arr_first_name = rq_first_name.split()
        rq_hr_first_name= arr_first_name[0]
        rq_hr_first_name = rq_hr_first_name.title()
        rq_hr_middle_name = arr_first_name[1:]
        rq_hr_middle_name = rq_hr_middle_name.title()
        rq_birth_date = request.POST.get("birth_date")
        rq_social_security_number = request.POST.get("social_security_number")
        rq_drivers_license = request.POST.get("drivers_license")
        rq_current_address_1 = request.POST.get("current_address_1")
        rq_current_address_2 = request.POST.get("current_address_2")
        rq_current_city = request.POST.get("current_city")
        rq_current_country = request.POST.get("current_country")
        rq_current_zip = request.POST.get("current_zip") #
        rq_current_gender = request.POST.get("current_gender")
        rq_current_phone_number = request.POST.get("current_phone_number")
        rq_current_personal_email = request.POST.get("current_personal_email")
        rq_current_marital_status = request.POST.get("current_marital_status")
        rq_ethnicity = request.POST.get("ethnicity")
        rq_shareholder_status = request.POST.get("shareholder_status")
        rq_benefit_plan = request.POST.get("benefit_plan")
        datahr2 = Personal(CURRENT_FIRST_NAME = rq_hr_first_name, CURRENT_LAST_NAME = rq_last_name, CURRENT_MIDDLE_NAME = rq_hr_middle_name, BIRTH_DATE = rq_birth_date,
                           SOCIAL_SECURITY_NUMBER = rq_social_security_number, DRIVERS_LICENSE = rq_drivers_license, CURRENT_ADDRESS_1 = rq_current_address_1, CURRENT_ADDRESS_2 = rq_current_address_2,
                           CURRENT_CITY = rq_current_city, CURRENT_COUNTRY = rq_current_country, CURRENT_ZIP = rq_current_zip, CURRENT_GENDER = rq_current_gender, CURRENT_PHONE_NUMBER = rq_current_phone_number,
                           CURRENT_PERSONAL_EMAIL = rq_current_personal_email, CURRENT_MARITAL_STATUS = rq_current_marital_status, ETHNICITY = rq_ethnicity, SHAREHOLDER_STATUS = rq_shareholder_status, BENEFIT_PLANS_ID = rq_benefit_plan)

        return render(request, "overview_app/changeemployee_detail.html")
    else:
        employees = Employee.objects.all()
        payrate = PayRate.objects.all()
        benefit_plans = BenefitPlans.objects.all()
        context = {'employees': employees, 'payrate': payrate, 'benefit_plans' : benefit_plans}
        return render(request, 'overview_app/Add_employee.html', context)