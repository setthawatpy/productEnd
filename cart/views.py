from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
from cart.models import Cart, CartItem


def createCart(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url="login")
def cart(request):
    counter = 0
    charge = 0
    total = 0
    netTotal = 0
    try:
        # ดึงข้อมูลตะกร้าสินค้า
        cart = Cart.objects.get(cart_id=createCart(request), employee=request.user)
        # ดึงข้อมูลสินค้าในตะกร้า
        cartItem = CartItem.objects.filter(cart=cart)
        # คำนวณราคาสินค้า
        for item in cartItem:
            # ปริมาณสิค้าทั้งหมดที่อยู่ในตะกร้า += จำนวนสินค้าที่อยู่ในตะกร้า
            counter += item.quantity
            charge += item.sub_charge()
            total += item.sub_total()
        netTotal = charge + total
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        cart = None
        cartItem = None
    context = {
        'cartItem': cartItem,
        'total': total,
        'counter': counter,
        'charge': charge,
        'netTotal': netTotal
    }
    return render(request, 'cart/cart.html', context)


def addCart(request, id):
    # product=Products.objects.get(id=id)
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


@login_required(login_url="login")
def removeCart(request, id):
    # ดึงข้อมูลตะกร้าสินค้า
    cart = Cart.objects.get(cart_id=createCart(request), employee=request.user)
    # ดึงข้อมูลสินค้า
    product = get_object_or_404(Product, id=id)
    # ดึงข้อมูลสินค้าที่อยู่ในตะกร้าสินค้า
    cartItem = get_object_or_404(CartItem, product=product, cart=cart)  # สินค้าที่ต้องการลบ
    cartItem.delete()
    return redirect('cart')
