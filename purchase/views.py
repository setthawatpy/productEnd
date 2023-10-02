from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from purchase.models import *
from purchase.forms import *
from general.models import Shop
from django.contrib import messages
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required(login_url="login")
def createPurchases(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.employee = request.user
            purchase.save()
            purchaseDetail = PurchaseDetail.objects.create(purchase=purchase)
            purchaseDetail.save()
            messages.success(request, "บันทึกรายการสำเร็จ")
            return redirect('purchasesList')
        else:
            print("Form Errors:", form.errors)
    else:
        form = PurchaseForm()
    context = {'form': form}
    return render(request, "purchase/createPurchases.html", context)


@login_required(login_url="login")
def editPurchases(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    if request.method == "POST":
        form = PurchaseForm(instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, "อัพเดทรายการสำเร็จ")
            return redirect("purchasesList")
        else:
            print("Form Errors:", form.errors)
            messages.error(request, "อัพเดทรายการสำเร็จล้มเหลว")
            return redirect("editPurchases")
    else:
        form = PurchaseForm(instance=purchase)
        date = purchase.get_date()
        time = purchase.get_time()
    context = {
            'form': form,
            'purchase': purchase,
            'date': date,
            'time': time
        }
    return render(request, "purchase/editPurchases.html", context)


@login_required(login_url="login")
def deletePurchases(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    purchase.delete()
    return redirect("purchasesList")


def purchasesList(request):
    purchases = Purchase.objects.all().order_by('date_time').reverse()
    count = purchases.count()
    context = {
        'purchases': purchases,
        'count': count
    }
    return render(request, "purchase/purchasesList.html", context)


def purchasesDetail(request, id):
    purchaseDetail = get_object_or_404(Purchase, id=id)
    context = {'purchaseDetail': purchaseDetail}
    return render(request, "purchase/purchasesDetail.html", context)


def purchaseReceipt(request, id):
    shops = Shop.objects.get(id=1)
    purchases = Purchase.objects.get(id=id)
    purchaseDetail = PurchaseDetail.objects.filter(purchase=purchases)
    context = {
        'purchaseDetail': purchaseDetail,
        'purchases': purchases,
        'shops': shops
    }
    return render(request, 'purchase/purchaseReceipt.html', context)


def search_purchases(request):
    search = request.GET.get('search')
    if search:
        purchases = Purchase.objects.filter(date_time__icontains=search)
        if not purchases:
            messages.error(request, 'ไม่พบข้อมูล')
            return redirect('purchasesList')
    else:
        return redirect('purchasesList')
    context = {'purchases': purchases}
    return render(request, "purchase/purchasesList.html", context)


def render_pdf_view(request, id):
    shops = Shop.objects.get(id=1)
    purchases = Purchase.objects.get(id=id)
    purchaseDetail = PurchaseDetail.objects.filter(purchase=purchases)
    
    template_path = 'purchase/pdf.html'
    context = {
        'purchaseDetail': purchaseDetail,
        'purchases': purchases,
        'shops': shops,
        'request': request  # ส่ง request เข้าไปใน context
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="purchases_report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf(request, id):
    # ดึงข้อมูลที่ต้องการแสดงใน PDF จากฐานข้อมูล
    shops = Shop.objects.get(id=1)
    purchases = Purchase.objects.get(id=id)
    purchaseDetail = PurchaseDetail.objects.filter(purchase=purchases)

    # สร้าง HTML จาก Template
    template = get_template('purchase/pdf.html')
    context = {'purchaseDetail': purchaseDetail, 'purchases': purchases, 'shops': shops, 'request': request}
    html = template.render(context)
    
    font_path = 'static/assets/fonts/fontsarabun/THSarabun.ttf'
    font_config = pisaFontConfig()
    font_config.addFont(font_path, "TH SarabunPSK")

    # สร้าง PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8', font_config=font_config)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="purchase_receipt.pdf"'
        return response
    else:
        return HttpResponse('เกิดข้อผิดพลาดในการสร้าง PDF')
