from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q
from account.models import *
from account.forms import *

# ********************************* Customer ************************************


@login_required(login_url="login")
def createCustomers(request):
    if request.method == 'POST':
        form = CustomersForm(request.POST, request.FILES)
        # ตรวจสอบความถูกต้องของข้อมูลฟอร์ม
        if form.is_valid():

            # ดึงค่ารหัสผ่านที่ผู้ใช้กรอกในฟอร์ม
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # เช็คปรียบเทียบรหัสผ่านที่รับมาจากฟอร์ม
            if password1 != password2:
                messages.error(request, 'รหัสผ่านไม่ตรงกัน')
                form.cleaned_data['password1'] = ''
                form.cleaned_data['password2'] = ''
                return render(request, 'account/customer/createCustomers.html', context)

            # บันทึกข้อมูลลูกค้าในตาราง Customers
            form.save()

            # ดึงค่ารหัสผ่านที่ผู้ใช้กรอกในฟอร์ม
            username = request.POST['id']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = ''
            password = request.POST['password1']

            # สร้าง User ในระบบ Django
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = False
            user.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ')
            return redirect('customersList')
        else:
            # เช็คชื่อผู้ใช้ซ้ำกับฐานข้อมูล
            username = request.POST['id']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'ชื่อผู้ใช้ซ้ำกับผู้ใช้ที่มีอยู่แล้ว')
                return redirect('createCustomers')
    else:
        form = CustomersForm()
    context = {'form': form}
    return render(request, 'account/customer/createCustomers.html', context)


@login_required(login_url="login")
def editCustomers(request, id):
    customers = get_object_or_404(Customer, id=id)
    status = customers.status  # บันทึกสถานะเดิมก่อนที่จะแก้ไข

    if request.method == 'POST':
        form = CustomersForm(request.POST, request.FILES, instance=customers)
        if form.is_valid():
            customers.set_active(True)
            form.save()

            # อัปเดตข้อมูลในตาราง User (ถ้าต้องการ)
            user = User.objects.get(username=customers.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # ให้สถานะเป็นค่าเดิมหลังจากอัปเดตเสร็จ
            if status:  # ถ้าสถานะเดิมเป็น True
                customers.set_active(True)
            else:
                customers.set_active(False)

            messages.success(request, 'อัปเดตข้อมูลลูกค้าสำเร็จ')
            return redirect('customersList')
        else:
            messages.error(request, 'เกิดข้อผิดพลาดในการอัปเดตข้อมูลลลูกค้า')
            return redirect('editCustomers')
    else:
        form = CustomersForm(instance=customers)
    context = {'form': form, 'customers': customers}
    return render(request, 'account/customer/editCustomers.html', context)


@login_required(login_url="login")
def deleteCustomers(request, id):
    customers = get_object_or_404(Customer, id=id)
    customers.delete()  # ลบข้อมูลลูกค้า

    # ลบผู้ใช้งานในตาราง User (ถ้าต้องการ)
    user = User.objects.filter(username=customers.id)
    user.delete()
    messages.success(request, 'ลบข้อมูลลูกค้าสำเร็จ')
    return redirect('customersList')


def customersList(request):
    customers = Customer.objects.all().order_by('id').reverse()
    count = customers.count()
    context = {
        'customers': customers,
        'count': count
    }
    return render(request, 'account/customer/customersList.html', context)


def customersProfile(request, id):
    customers = get_object_or_404(Customer, id=id)
    context = {'customers': customers}
    return render(request, 'account/customer/customersProfile.html', context)


def activate_customers(request, id):
    customers = get_object_or_404(Customer, id=id)
    status = request.GET.get('status')
    if status == 'open':
        customers.set_active(True)
    elif status == 'close':
        customers.set_active(False)
    print(status)
    return redirect('customersList')


def search_customers(request):
    search = request.GET.get('search')
    if search:
        customers = Customer.objects.filter(Q(first_name__icontains=search) | Q(id=search))
    else:
        return redirect('employeesList')
    context = {'customers': customers}
    return render(request, "account/customer/customersList.html", context)


# *******************************************************************************

# ********************************* Employee ************************************

@login_required(login_url="login")
def createEmployees(request):
    if request.method == 'POST':
        form = EmployeesForm(request.POST, request.FILES)
        # ตรวจสอบความถูกต้องของข้อมูลฟอร์ม
        if form.is_valid():

            # ดึงค่ารหัสผ่านที่ผู้ใช้กรอกในฟอร์ม
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # เช็คปรียบเทียบรหัสผ่านที่รับมาจากฟอร์ม
            if password1 != password2:
                messages.error(request, 'รหัสผ่านไม่ตรงกัน')
                form.cleaned_data['password1'] = ''
                form.cleaned_data['password2'] = ''
                return render(request, 'account/employee/createEmployees.html', context)

            # บันทึกข้อมูลพนักงานในตาราง Employees
            form.save()

            # ดึงค่ารหัสผ่านที่ผู้ใช้กรอกในฟอร์ม
            username = request.POST['id']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = ''
            password = request.POST['password1']

            # สร้าง User ในระบบ Django
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True
            user.save()
            messages.success(request, 'เพิ่มพนักงานสำเร็จ')
            return redirect('employeesList')
        else:
            # เช็คชื่อผู้ใช้ซ้ำกับฐานข้อมูล
            username = request.POST['id']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'ชื่อผู้ใช้ซ้ำกับผู้ใช้ที่มีอยู่แล้ว')
                return redirect('createEmployees')
    else:
        form = EmployeesForm()
    context = {'form': form}
    return render(request, 'account/employee/createEmployees.html', context)


@login_required(login_url="login")
def editEmployees(request, id):
    employees = get_object_or_404(Employee, id=id)
    status = employees.status  # บันทึกสถานะเดิมก่อนที่จะแก้ไข

    if request.method == 'POST':
        form = EmployeesForm(request.POST, request.FILES, instance=employees)
        if form.is_valid():
            form.save()
            # อัปเดตข้อมูลในตาราง User (ถ้าต้องการ)
            user = User.objects.get(username=employees.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # ให้สถานะเป็นค่าเดิมหลังจากอัปเดตเสร็จ
            if status:  # ถ้าสถานะเดิมเป็น True
                employees.set_active(True)
            else:
                employees.set_active(False)

            messages.success(request, 'อัปเดตข้อมูลพนักงานสำเร็จ')
            return redirect('employeesList')
        else:
            messages.error(request, 'เกิดข้อผิดพลาดในการอัปเดตข้อมูลพนักงาน')
            return redirect('editEmployees')
    else:
        form = EmployeesForm(instance=employees)
    context = {'form': form, 'employees': employees}
    return render(request, 'account/employee/editEmployees.html', context)


@login_required(login_url="login")
def deleteEmployees(request, id):
    employees = get_object_or_404(Employee, id=id)
    employees.delete()  # ลบข้อมูลพนักงาน

    # ลบผู้ใช้งานในตาราง User (ถ้าต้องการ)
    user = User.objects.filter(username=employees.id)
    user.delete()
    messages.success(request, 'ลบข้อมูลพนักงานสำเร็จ')
    return redirect('employeesList')


def employeesList(request):
    employees = Employee.objects.all().order_by('id').reverse()
    count = employees.count()
    context = {
        'employees': employees,
        'count': count
    }
    return render(request, 'account/employee/employeesList.html', context)


def employeesProfile(request, id):
    employees = get_object_or_404(Employee, id=id)
    context = {'employees': employees}
    return render(request, 'account/employee/employeesProfile.html', context)


def activate_employees(request, id):
    employees = get_object_or_404(Employee, id=id)
    status = request.GET.get('status')
    if status == 'open':
        employees.set_active(True)
    elif status == 'close':
        employees.set_active(False)
    print(status)
    return redirect('employeesList')


def search_employees(request):
    search = request.GET.get('search')
    if search:
        employees = Employee.objects.filter(Q(first_name__icontains=search) | Q(id=search))
    else:
        return redirect('employeesList')
    context = {'employees': employees}
    return render(request, "account/employee/employeesList.html", context)

# *******************************************************************************

# ********************************* Authenticate ************************************


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == "" or password == "":
            messages.warning(request, "กรุณาป้อนข้อมูลให้ครบ")
            return redirect('login')
        else:
            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:
                # ตรวจสอบว่าเป็น superuser หรือไม่
                if user.is_superuser:
                    auth.login(request, user)
                    messages.success(request, "เข้าสู่ระบบสำเร็จ")
                    return redirect('index')

                # ตรวจสอบสถานะของผู้ใช้งานในตาราง Customer
                try:
                    customer = Customer.objects.get(id=username)
                    if customer.status:
                        auth.login(request, user)
                        messages.success(request, "เข้าสู่ระบบสำเร็จ")
                        return redirect('index')
                    else:
                        messages.error(
                            request, "ไม่สามารถเข้าสู่ระบบได้ เนื่องจากบัญชีถูกปิดการใช้งาน")
                        return redirect('login')
                except Customer.DoesNotExist:

                    # ตรวจสอบสถานะของผู้ใช้งานในตาราง Employee
                    try:
                        employee = Employee.objects.get(id=username)
                        if employee.status:
                            auth.login(request, user)
                            messages.success(request, "เข้าสู่ระบบสำเร็จ")
                            return redirect('index')
                        else:
                            messages.error(
                                request, "ไม่สามารถเข้าสู่ระบบได้ เนื่องจากบัญชีถูกปิดการใช้งาน")
                            return redirect('login')
                    except Employee.DoesNotExist:
                        messages.error(request, "ไม่พบข้อมูลบัญชีผู้ใช้งาน")
                        return redirect('login')
            else:
                messages.error(request, "ไม่พบข้อมูลบัญชีผู้ใช้งาน")
                return redirect('login')
    else:
        return render(request, 'account/login.html')


@login_required(login_url="login")
def logout_user(request):
    auth.logout(request)
    messages.success(request, "ออกจากระบบสำเร็จ")
    return redirect('index')


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            # เช็ครหัสผ่านเดิม
            user = authenticate(
                username=request.user.username, password=old_password)
            if user is not None:
                # รหัสผ่านตรงกัน
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'รหัสผ่านถูกเปลี่ยนแปลงสำเร็จ')
                    return redirect('home')
                else:
                    # รหัสผ่านไม่ตรงกัน
                    messages.error(
                        request, 'รหัสผ่านใหม่ และยืนยันรหัสผ่านไม่ตรงกัน')
                    return redirect('changPassword')
            else:
                messages.error(request, 'รหัสผ่านเดิมไม่ถูกต้อง')
                return redirect('changPassword')
        else:
            messages.error(request, 'รหัสผ่านใหม่ และยืนยันรหัสผ่านไม่ตรงกัน')
            return redirect('changPassword')
    else:
        form = ChangePasswordForm()
    context = {'form': form}
    return render(request, 'account/changPassword.html', context)
