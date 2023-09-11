from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderDetail
from product.models import Product
from cart.models import Cart, CartItem
from cart.views import createCart
from django.contrib import messages


@login_required(login_url="/login")
def order(request):
    counter = 0
    charge = 0
    total = 0
    netTotal = 0

    # ดึงข้อมูลตะกร้าสินค้า
    cart = Cart.objects.get(cart_id=createCart(request), employee=request.user)
    # ดึงข้อมูลสินค้าในตะกร้า
    cartItem = CartItem.objects.filter(cart=cart)
    for item in cartItem:
        counter += item.quantity
        charge += item.sub_charge()
        total += item.sub_total()
    netTotal = charge + total

    # สร้างใบสั่งซื้อ
    order = Order.objects.create(employee=request.user, total=total, charge=charge, netTotal=netTotal)
    order.save()

    # บันทึกรายการสั่งซื้อ และตัด Stock
    for item in cartItem:
        orderDetail = OrderDetail.objects.create(
            order=order,
            product=item.product.title,
            charge=item.product.charge,
            price=item.product.price,
            quantity=item.quantity,
        )
        orderDetail.save()

        # ตัด Stock
        product = Product.objects.get(id=item.product.id)
        product.stock = (item.product.stock - orderDetail.quantity)
        product.save()
        item.delete()

    cart.delete()
    messages.success(request, "สั่งซื้อสินค้าสำเร็จ")
    return redirect("orderHistory")


@login_required(login_url="/login")
def orderHistory(request):
    order = Order.objects.filter(employee=request.user).order_by('date_time').reverse()
    count = order.count()
    context = {
        'order': order,
        'count': count
    }
    return render(request, "order/orderHistory.html", context)


@login_required(login_url="/login")
def invoice(request, id):
    order = Order.objects.get(id=id)
    orderDetail = OrderDetail.objects.filter(order=order)
    context = {
        'order': order,
        'orderDetail': orderDetail
    }
    return render(request, "order/invoice.html", context)
