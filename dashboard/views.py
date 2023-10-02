from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.db.models import Sum
from decimal import Decimal
from account.models import *
from general.models import *
from cart.models import *
from contract.models import *
from order.models import *
from product.models import *
from purchase.models import *


def calculate_total_price(products):
    total_price = Decimal('0.00')  # ตั้งค่าราคารวมเริ่มต้นเป็น 0.00
    for product in products:
        total_price += product.price  # เพิ่มราคาของสินค้าแต่ละชิ้นเข้าไปในราคารวม

    return total_price


def dashboard(request):
    category  = Category.objects.all()
    category_count = category.count()
    
    product = Product.objects.all()
    product_count = product.count()

    total_price = calculate_total_price(product)
    
    order = Order.objects.all()
    order_count = order.count()
    
    order_detail = OrderDetail.objects.all()
    order_detail_count = order_detail.count()
    total_sales = Order.objects.aggregate(total_sales=Sum('total'))['total_sales']
    total_sold_quantity = OrderDetail.objects.aggregate(total_sold_quantity=Sum('quantity'))['total_sold_quantity']
    context = {
        'category': category,
        'category_count': category_count,
        
        'product': product,
        'product_count': product_count,
        
        'total_price': total_price,
        
        'order': order,
        'order_count': order_count,
        
        'order_detail': order_detail,
        'order_detail_count': order_detail_count,
        'total_sales': total_sales,
        'total_sold_quantity': total_sold_quantity,
    }

    return render(request, 'dashboard/dashboard.html', context)


def report_account(request):
    employee = Employee.objects.all()
    employee_count = employee.count()
    employee_male = Employee.objects.filter(gender='ชาย').count()
    employee_female = Employee.objects.filter(gender='หญิง').count()
    customer = Customer.objects.all()
    customer_count = customer.count()
    customer_male = Customer.objects.filter(gender='ชาย').count()
    customer_female = Customer.objects.filter(gender='หญิง').count()
    
    total_count = employee_count + customer_count
    total_male = employee_male + customer_male
    total_female = employee_female + customer_female
    context = {
        'employee': employee,
        'employee_count': employee_count,
        'customer': customer,
        'customer_count': customer_count,
        'total_count': total_count,
        'employee_male': employee_male,
        'employee_female': employee_female,
        'customer_male': customer_male,
        'customer_female': customer_female,
        'total_male': total_male,
        'total_female': total_female,
    }
    return render(request, 'dashboard/reportAccount.html', context)


def report_product(request):
    category  = Category.objects.all()
    category_count = category.count()
    
    product = Product.objects.all()
    product_count = product.count()
    context = {
        'category': category,
        'category_count': category_count,
        'product': product,
        'product_count': product_count,
    }
    return render(request, 'dashboard/reportProduct.html', context)


def report_purchase(request):
    purchase = Purchase.objects.all()
    purchase_count = purchase.count()
    context = {
        'purchase': purchase,
        'purchase_count': purchase_count,
    }
    return render(request, 'dashboard/reportPurchase.html', context)


def report_sales(request):
    cart = Cart.objects.all()
    cart_count = cart.count()
    
    cart_item = CartItem.objects.all()
    cart_item_count = cart_item.count()
    
    order = Order.objects.all()
    order_count = order.count()
    
    order_detail = OrderDetail.objects.all()
    order_detail_count = order_detail.count()
    
    context = {
        'cart': cart,
        'cart_count': cart_count,
        
        'cart_item': cart_item,
        'cart_item_count': cart_item_count,
        
        'order': order,
        'order_count': order_count,
        
        'order_detail': order_detail,
        'order_detail_count': order_detail_count,
    }
    return render(request, 'dashboard/reportSales.html', context)


def report_contract(request):
    contract = Contract.objects.all()
    contract_count = contract.count()
    
    item = Item.objects.all()
    item_count = item.count()
    
    repayment = Repayment.objects.all()
    repayment_count = repayment.count()
    
    context = {
        'contract': contract,
        'contract_count': contract_count,
        'item': item,
        'item_count': item_count,
        'repayment': repayment,
        'repayment_count': repayment_count,
    }
    return render(request, 'dashboard/reportContract.html', context)