from cart.models import Cart, CartItem
from cart.views import createCart

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:    
            cart = Cart.objects.filter(cart_id=createCart(request))
            cart_Item = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_Item:
                item_count += item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)