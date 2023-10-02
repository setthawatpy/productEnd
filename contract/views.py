from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date, timedelta
from contract.models import *
from contract.forms import *
import time
import requests
import locale
import schedule




@login_required(login_url="login")
def createContract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.employee = request.user
            contract.save()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect('create_item', id=contract.id)
        else:
            messages.error(request, 'บันทึกข้อมูลไม่สำเร็จ')
    else:
        form = ContractForm()
    context = {'form': form}
    return render(request, 'contract/createContracts.html', context)


@login_required(login_url="login")
def create_item(request, id):
    contract = get_object_or_404(Contract, id=id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.contract = contract
            item.save() 
            
            # คำนวณค่า total_weight และ total_price ของ items ในสัญญา
            items = Item.objects.filter(contract=contract)
            t_weight = sum(item.weight for item in items)
            t_price = sum(item.price for item in items)
            
            contract.total_weight = t_weight
            contract.total_price = t_price
            contract.save()

            messages.success(request, 'บันทึกสำเร็จ')
            return redirect('create_item', id=id)
        else:
            messages.error(request, 'บันทึกข้อมูลไม่สำเร็จ')
            return redirect('create_item', id=id)
    else:
        form = ItemForm()
    items = Item.objects.filter(contract=contract)
    context = {
        'form': form,
        'contract': contract,
        'items': items,
    }
    return render(request, 'contract/createItem.html', context)


@login_required(login_url="login")
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    contract = item.contract
    # โดยตรวจสอบว่า Item นี้อยู่ในสัญญาที่ถูกต้องหรือไม่
    if item.contract == item.contract:
        item.delete()
        
        # ดึงรายการ items ที่เป็นของ contract
        items = Item.objects.filter(contract=contract)

        # คำนวณ t_weight และ t_price
        t_weight = sum(item.weight for item in items)
        t_price = sum(item.price for item in items)

        # อัปเดตค่า total_weight และ total_price ของ contract
        contract.total_weight = t_weight
        contract.total_price = t_price
        contract.save()
        messages.success(request, 'ลบสินค้าสำเร็จ')
    else:
        messages.error(request, 'ไม่สามารถลบสินค้าได้')
    return redirect('create_item', id=item.contract.id)


@login_required(login_url="login")
def editContract(request, id):
    contracts = Contract.objects.get(id=id)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contracts)
        if form.is_valid():
            form.save()
            messages.success(request, "อัพเดทข้อมูลสำเร็จ")
            # เปลี่ยนเส้นทาง URL ไปยังหน้ารายการสัญญา
            return redirect('contractsList')
        else:
            messages.error(request, "อัพเดทข้อมูลล้มเหลว")

    else:
        form = ContractForm(instance=contracts)
    context = {'form': form}
    return render(request, 'contract/editContracts.html', context)


def calculator_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    period = int(contract.period) # งวด
    loan = contract.total_price   # เงินกู้
    
    interest_rate = contract.interest_rate  # อัตราดอกเบี้ยต่อปี
    interest_total = 0
    loan_total = 0
    # วิธีคิดดอกเบี้ยเงินกู้แบบลดต้นลดดอก
    
    # อัตราดอกเบี้ยต่อเดือน = (อัตราดอกเบี้ยต่อปี /100) / จำนวนวันในงวด / 365
    int_rate =  (interest_rate/ 100) * 30 / 365         
    result1 = (1 / (1 + int_rate) ** period)
    result2 = (1 - result1) / int_rate  
    
    # ยอดชำระต่อเดือน 
    monthly_payment = loan / result2
    
    for i in range(1, period + 1):
        
        # ดอกเบี้ยต่องวด    = เงินต้น * อัตราดอกเบี้ยต่อเดือน
        monthly_interest = loan * int_rate
        
        # ชำระเงินต้นต่องวด = ยอดชำระต่อเดือน -  ดอกเบี้ยต่องวด
        reduced_principal = monthly_payment - monthly_interest
        
        # เงินต้นคงเหลือ -= ยอดชำระต่อเดือน
        loan -= reduced_principal
        
        # รวมดอกเบี้ยทั้งหมด += ยอดชำระต่อเดือน
        interest_total += monthly_interest
        
        # รวมชำระเงินต้นต่องวด += ชำระเงินต้นต่องวด
        loan_total += reduced_principal
        
        # กำหนดค่า due_date ให้เป็นวันที่ 30 ของเดือนนั้นๆ
        year = contract.date_time.year + 543
        month = contract.date_time.month + i - 1
        
        # ตรวจสอบว่าเดือนไม่เกิน 12
        if month > 12:
            year += 1
            month -= 12
            
        # ตรวจสอบว่าวันที่ 30 เป็นวันที่ถูกต้องสำหรับเดือนนี้
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31
        elif month == 2:
            day = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
        else:
            day = 30
        due_date = date(year, month, day)
        
        contract.total_interest = interest_total
        contract.total_loan = loan_total
        contract.save()
        repayment = Repayment.objects.create(contract=contract, month=i)
        repayment.due_date = due_date                                           # วันครบกำหนด
        repayment.monthly_installments = monthly_payment                        # ผ่อนชำระรายเดือน
        repayment.monthly_interest = monthly_interest                           # ดอกเบี้ย / เดือน
        repayment.monthly_payment = reduced_principal                           # เงินต้น / เดือน
        repayment.remaining_principal = loan                                    # เงินต้นที่เหลืออยู่
        repayment.save()
    return redirect('contract_detail', id=id)


def contractsList(request):
    contracts = Contract.objects.all().order_by('id').reverse()
    count = contracts.count()
    context = {
        "contracts": contracts,
        "count": count,
    }
    return render(request, "contract/contractsList.html", context)


def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    items = Item.objects.filter(contract=contract)
    repayments = Repayment.objects.filter(contract=contract)
    count = items.count()
    context = {
        'contract': contract,
        'items': items,
        'repayments': repayments,
        'count': count,
    }
    return render(request, 'contract/contractsDetail.html', context)


def search_contract(request):
    search = request.GET.get('search')
    if search:
        contracts = Contract.objects.filter(id=search)
    else:
        return redirect('contractsList')
    context = {'contracts': contracts}
    return render(request, "contract/contractsList.html", context)


def notificationList(request):
    contracts = Contract.objects.all().order_by('id').reverse()
    count = contracts.count()
    context = {
        "contracts": contracts,
        "count": count,
    }
    return render(request, "contract/notifications/notificationList.html", context)


def notification_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    repayments = Repayment.objects.filter(contract=contract)
    context = {
        'contract': contract,
        'repayments': repayments
    }
    return render(request, "contract/notifications/notificationDetail.html", context)


def send_line_notify(request):
    if request.method == 'POST':
        send = request.POST.get('send')
        repayment = get_object_or_404(Repayment, id=send)
        url = 'https://notify-api.line.me/api/notify'
        token = 'Vw1Qu02ctanSRAMGjw12vretJ4o3mEDffw9J0pRwTRR'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + token
        }
        locale.setlocale(locale.LC_ALL, 'th_TH')
        monthly_installments = repayment.monthly_installments
        formatted_due_date = repayment.due_date.strftime('%d %B %Y')
        formatted_monthly_installments = locale.format_string('%.2f', monthly_installments, grouping=True)
        message =   f'\n'\
                    f'เลขที่สัญญา {repayment.contract.id}\n' \
                    f'ชื่อ {repayment.contract.customer.first_name} {repayment.contract.customer.last_name}\n' \
                    f'แจ้งชำระค่างวดเดือนที่ {repayment.month}\n' \
                    f'วันครบกำหนด: {formatted_due_date}\n' \
                    f'ยอดชำระเดือนนี้: {formatted_monthly_installments + " บาท"} \n'
        data = {'message': message}
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print("ส่งข้อความสำเร็จ")
        else:
            print("เกิดข้อผิดพลาด ไม่สามารถส่งข้อความได้")
            
    messages.success(request, "ส่งข้อความแจ้งเตือนสำเร็จ")
    return redirect('notification_detail', id=repayment.contract.id)


def paymentList(request):
    contracts = Contract.objects.all().order_by('id').reverse()
    count = contracts.count()
    context = {
        "contracts": contracts,
        "count": count,
    }
    return render(request, "contract/payments/paymentList.html", context)


def payment_installment(request, id):
    contract = get_object_or_404(Contract, id=id)
    repayments = Repayment.objects.filter(contract=contract)
    context = {
        'contract': contract,
        'repayments': repayments
    }
    return render(request, "contract/payments/paymentInstallment.html", context)


def payment_details(request, id):
    repayments = get_object_or_404(Repayment, id=id)
    return render(request, "contract/payments/paymentDetails.html", {'repayments': repayments})


@login_required(login_url="login")
def confirm_payment(request, id):
    repayment = get_object_or_404(Repayment, id=id)
    if request.method == 'POST':
        form = PaymentsForm(request.POST, request.FILES, instance=repayment)
        if form.is_valid():
            form.instance.status = True
            form.save()
            messages.success(request, "อัพโหลดสลีปโอนเงินสำเร็จ")
            repayment.contract.check_payments()
            return redirect('payment_installment', id=repayment.contract.id)
        else:
            messages.error(request, "อัพโหลดสลีปโอนเงินล้มเหลว")
    else:
        repayment = get_object_or_404(Repayment, id=id) 
        form = PaymentsForm(instance=repayment)
    context = {
        'form': form,
        'repayment': repayment,
    }
    return render(request, "contract/payments/confirmPayment.html", context)


def redemption_list(request):
    contracts = Contract.objects.all().order_by('id').reverse()
    count = contracts.count()
    context = {
        "contracts": contracts,
        "count": count,
    }
    return render(request, "contract/redemption/redemptionList.html", context)


def confirm_redemption(request, id):
    contract = get_object_or_404(Contract, id=id)
    if contract.contract_status:
        contract.redemption_status = True
        contract.save()
        messages.success(request, "ไถ่ถอนทองคำสำเร็จ")
        return redirect('redemption_items')
    else:
        messages.error(request, "ไม่สามารถยืนยันการไถ่ถอนได้ เนื่องจากสัญญาอยู่ในช่วงชำระค่างวด")
    return redirect('redemption_items')


def redemption_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    items = Item.objects.filter(contract=contract)
    repayments = Repayment.objects.filter(contract=contract)
    count = items.count()
    context = {
        'contract': contract,
        'items': items,
        'repayments': repayments,
        'count': count,
    }
    return render(request, "contract/redemption/redemptionDetail.html", context)






    # if not redemption.status:
                #     redemption.status = True
                #     redemption.save()
                #     messages.success(request, "ไถ่ถอนสำเร็จ")
                #     return redirect('redemption_items')
                # else:
                #     # หากมีรายการ Redemption และสถานะเป็น True แสดงว่าไถ่ถอนได้แล้ว
                #     messages.error(request, "ไถ่ถอนไม่สำเร็จได้แล้ว")
                #     return redirect('redemption_items')
    
    
    
    
    
# def confirm_payment(request, id):
#     repayment = get_object_or_404(Repayment, id=id)
#     contract = repayment.contract  # ดึงข้อมูลสัญญาจากการชำระเงิน

#     if request.method == 'POST':
#         form = PaymentsForm(request.POST, request.FILES, instance=repayment)
#         if form.is_valid():
#             form.instance.status = True
#             form.save()
#             messages.success(request, "อัพโหลดสลีปโอนเงินสำเร็จ")
#             return redirect('payment_show', id=repayment.contract.id)  # ใช้ contract.id เพื่อนำไปยังหน้า payment_show
#         else:
#             messages.error(request, "อัพโหลดสลีปโอนเงินล้มเหลว")
#     else:
#         form = PaymentsForm(instance=repayment)

#     repayments = Repayment.objects.filter(contract=contract)
#     if repayments.filter(status=True).count() == 1:
#         # ถ้าชำระครบทุกงวด ให้เปลี่ยนสถานะของสัญญาเป็น True
#         contract.status = True
#         contract.save()
#     context = {
#         'form': form,
#         'repayment': repayment,
#     }
#     return render(request, "contract/confirmPayment.html", context)





# def send_line_notify(request):
#     if request.method == 'POST':
#         url = 'https://notify-api.line.me/api/notify'
#         token = 'Vw1Qu02ctanSRAMGjw12vretJ4o3mEDffw9J0pRwTRR'  # ใส่ Access Token ที่คุณได้จาก LINE Notify
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Authorization': 'Bearer ' + token
#         }
#         message = 'Hello from Django using LINE Notify!'
#         data = {'message': message}

#         response = requests.post(url, headers=headers, data=data)
#         if response.status_code == 200:
#             print("ส่งข้อความสำเร็จ")
#         else:
#             print("เกิดข้อผิดพลาด ไปทำมาใหม่ไอ่โง่")
    
#     # คุณอาจจะต้องเพิ่มการคืน HttpResponse ในกรณีอื่น ๆ ด้วย
#     messages.success(request, "ส่งข้อความสำเร็จ")
#     return HttpResponse("ส่ง LINE Notification สำเร็จ")




# while True:
#     schedule.run_pending()
#     time.sleep(1)       
            
# def send_line_notify(request):
#     if request.method == 'POST':
#         url = 'https://notify-api.line.me/api/notify'
#         token = '4R7iXyMcOBSgNU899KEEv1WsYxY1ib4tjtYj0AFd0YE'  # ใส่ Access Token ที่คุณได้จาก LINE Notify
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Authorization': 'Bearer ' + token
#         }
#         message = 'Hello from Django using LINE Notify!'
#         data = {'message': message}

#         response = requests.post(url, headers=headers, data=data)
#         if response.status_code == 200:
#             print("ส่งข้อความสำเร็จ")
#         else:
#             print("เกิดข้อผิดพลาด ไปทำมาใหม่ไอ่โง่")

# price = 0
# while True:
#     url = 'https://api.chnwt.dev/thai-gold-apilatest'
#     response = requests.get(url)
#     data = response.json()
#     day = data['response'],['data']
#     times = data['response']['update_time']
#     gold_buy = data['response']['price']['gold']['buy']
#     gold_sell = data['response']['price']['gold']['sell']
#     goldBar_buy = data['response']['price']['gold_bar']['buy']
#     goldBar_sell = data['response']['price']['gold_bar']['sell']
#     change = data['response']['price']['change']['compare_previous']

#     last = gold_buy
#     if price != last:
#         message =   f"{day} \n"\
#                 f"{times} \n"\
#                 f"{gold_buy} \n"\
#                 f"{gold_sell} \n"\
#                 f"{goldBar_buy} \n"\
#                 f"{goldBar_sell} \n"\
#                 f"{change} \n"
#         message = {'message': message}
#         send_line_notify(message)
#         price = last

# def sendLineNotification(data):
#     url = 'https://notify-api.line.me/api/notify'
#     token = 'Vw1Qu02ctanSRAMGjw12vretJ4o3mEDffw9J0pRwTRR'  # ใส่ Access Token ที่คุณได้จาก LINE Notify
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Authorization': 'Bearer ' + token
#     }

#     response = requests.post(url, headers=headers, data=data)

#     if response.status_code == 200:
#         print("ส่งข้อความสำเร็จ")
#     else:
#         print("เกิดข้อผิดพลาด ไปทำมาใหม่ไอ่โง่")


# price = 0
# while True:
#     url = 'https://api.chnwt.dev/thai-gold-apilatest'
#     response = requests.get(url)
#     data = response.json()

#     day = data['response']['date']
#     times = data['response']['update_time']
#     gold_buy = data['response']['price']['gold']['buy']
#     gold_sell = data['response']['price']['gold']['sell']
#     goldBar_buy = data['response']['price']['gold_bar']['buy']
#     goldBar_sell = data['response']['price']['gold_bar']['sell']
#     change = data['response']['price']['change']['compare_previous']

#     last = gold_buy
#     if price != last:
#         message =   f"{day} \n"\
#                     f"{times} \n"\
#                     f"-------------------- \n"\
#                     f"ทองคำรูปพรรณ : รับซื้อ {gold_buy} \n"\
#                     f"ทองคำรูปพรรณ : ขายออก {gold_sell} \n"\
#                         f"-------------------- \n"\
#                     f"ทองคำแท่ง : รับซื้อ {goldBar_buy} \n"\
#                     f"ทองคำแท่ง : ขายออก {goldBar_sell} \n"\
#                         f"-------------------- \n"\
#                     f"{change} \n"\
#                     f"-------------------- \n"

#         data = {'message': message}
#         sendLineNotification(data)
#         price = last # ราคาใหม่

#     # ทำการหน่วงเวลาหรือ sleep ไว้ เพื่อไม่ให้ทำงานซ้ำๆ อย่างรวดเร็ว
#     time.sleep(60)  # หน่วงเวลา 1 นาที
