from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from purchase.models import *
from purchase.forms import *
from django.contrib import messages


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
    purchases = Purchase.objects.get(id=id)
    purchaseDetail = PurchaseDetail.objects.filter(purchase=purchases)
    context = {
        'purchaseDetail': purchaseDetail,
        'purchases': purchases
        }
    return render(request, 'purchase/purchaseReceipt.html', context)


from datetime import datetime
def search_purchases(request):
    search = request.GET.get('search')
    if search:
        try:
            search_date = datetime.strptime(search, '%Y-%m-%d').date()
        except ValueError:
            return redirect('purchasesList')
        purchases = Purchase.objects.filter(date_time__date=search_date )
    else:
        return redirect('purchasesList')
    context = {'purchases': purchases}
    return render(request, "purchase/purchasesList.html", context)