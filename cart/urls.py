from django.urls import path
from cart import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_cart/<id>',views.add_cart, name='add_cart'),
    path('reduce_cart/<id>',views.reduce_cart, name='reduce_cart'),
    path('remove_cart/<id>',views.remove_cart, name='remove_cart'),
    
]
