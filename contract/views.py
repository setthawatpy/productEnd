from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from contract.models import *
from contract.forms import *
from django.contrib import messages
from account.models import Customer
from django.db.models import Q
import requests
import time
import datetime
import schedule


def createContract(request):
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # บันทึกสัญญา
            form.save()
            messages.success(request, "บันทึกรายการสำเร็จ")
            return redirect('contractsList')
        else:
            messages.success(request, "ไม่สามารถบันทึกรายการได้")
            return redirect('createContracts')
    else:
        form = ContractForm()
    context = {'form': form}
    return render(request, "contract/createContracts.html", context)


def addItem(request):
    if request.method == "POST":
        form = ContractItemForm(request.POST)
        if form.is_valid():
            # บันทึกข้อมูลสินค้าในสัญญา\
            # form.save()
            # contractItem = form.save(commit=False)  # บันทึกรายการสินค้าแต่ยังไม่บันทึกเข้ากับสัญญา
            # # เชื่อมรายการสินค้ากับสัญญา
            # contractItem.contract = Contract.objects.last()  # นี่คือวิธีง่ายๆ เพื่อเลือกสัญญาล่าสุดที่ถูกสร้าง
            # contractItem.save()  # บันทึกรายการสินค้า
            messages.success(request, "บันทึกรายการสำเร็จ")
            return redirect('createContracts')
        else:
            messages.error(request, "ไม่สามารถบันทึกรายการได้")
    else:
        form = ContractItemForm()
    context = {
        'form': form,
        }
    return render(request, "contract/contractsItem.html", context)


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


def deleteContract(request, id):
    contracts = get_object_or_404(Contract, id=id)
    contracts.delete()
    return redirect("contractsList")


def contractList(request):
    contracts = Contract.objects.all()
    context = {'contracts': contracts}
    return render(request, "contract/contractsList.html", context)


def search_contract(request):
    search = request.GET.get('search')
    if search:
        contracts = Customer.objects.filter(Q(date_time__icontains=search) | Q(id=search))
    else:
        return redirect('contractsList')
    context = {'contracts': contracts}
    return render(request, "contract/contractsList.html", context)




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
#             return HttpResponse('Notification sent successfully!')
#         else:
#             print("เกิดข้อผิดพลาด ไปทำมาใหม่ไอ่โง่")
#             return HttpResponse(f'Failed to send notification: {response.text}', status=500)
#     else:
#         return HttpResponse('Method not allowed', status=405)

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

    # # ทำการหน่วงเวลาหรือ sleep ไว้ เพื่อไม่ให้ทำงานซ้ำๆ อย่างรวดเร็ว
    # time.sleep(60)  # หน่วงเวลา 1 นาที
