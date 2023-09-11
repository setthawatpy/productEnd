from django.urls import path
from cart import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('addCart/<id>',views.addCart, name='addCart'),
    path('removeCart/<id>',views.removeCart, name='removeCart')
]
