from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
from cart.models import Cart, CartItem
from django.http import JsonResponse

def createCart(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url="login")
def cart(request):
    quantity = 0
    charge = 0
    total = 0
    net_total = 0
    try:
        # ดึงข้อมูลตะกร้าสินค้า
        cart = Cart.objects.get(cart_id=createCart(request), employee=request.user)
        # ดึงข้อมูลสินค้าในตะกร้า
        cartItem = CartItem.objects.filter(cart=cart)
        # คำนวณราคาสินค้า
        for item in cartItem:
            # ปริมาณสิค้าทั้งหมดที่อยู่ในตะกร้า += จำนวนสินค้าที่อยู่ในตะกร้า
            quantity += item.quantity
            charge += item.sub_charge()
            total += item.sub_total()
        net_total += total + charge
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        cart = None
        cartItem = None
    context = {
        'cartItem': cartItem,
        'quantity': quantity,
        'charge': charge,
        'total': total,
        'net_total': net_total,
    }
    return render(request, 'cart/cart.html', context)


def add_cart(request, id):
    product = get_object_or_404(Product, id=id)
    print(product)
    
    # สร้างตะกร้าสินค้า
    try:
        # มีตะกร้าสินค้า
        cart = Cart.objects.get(cart_id=createCart(request))
    except Cart.DoesNotExist:
        # ไม่มีตะกร้า
        cart = Cart.objects.create(cart_id=createCart(request), employee=request.user)
        cart.save()
        
    # บันทึกรายการสินค้าในตะกร้า
    try:
        # ซื้อสินค้าตัวเดิม
        cartitem = CartItem.objects.get(product=product, cart=cart)
        if cartitem.quantity < cartitem.product.stock:
            cartitem.quantity += 1
            cartitem.save()
    except CartItem.DoesNotExist:
        # ซื้อสินค้า
        cartitem = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cartitem.save()
    print(cartitem)
    return redirect('cart')


def reduce_cart(request, id):
    cart = Cart.objects.get(cart_id=createCart(request))
    product = get_object_or_404(Product, id=id)
    cartitem = CartItem.objects.get(product=product, cart=cart)
    if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()
    else:
        cartitem.delete()
    return redirect('cart')


@login_required(login_url="login")
def remove_cart(request, id):
    # ดึงข้อมูลตะกร้าสินค้า
    cart = Cart.objects.get(cart_id=createCart(request), employee=request.user)
    # ดึงข้อมูลสินค้า
    product = get_object_or_404(Product, id=id)
    # ดึงข้อมูลสินค้าที่อยู่ในตะกร้าสินค้า
    cartItem = get_object_or_404(CartItem, product=product, cart=cart)  # สินค้าที่ต้องการลบ
    cartItem.delete()
    return redirect('cart')


#         monthly_payment = contract.total_price / int(contract.period)
    #     monthly_interest = (contract.total_price * contract.interest_rate) * 30 / 365
    
    #     reduced_principal = monthly_payment - monthly_interest
    
    #     remaining_principal = contract.total_price - reduced_principal