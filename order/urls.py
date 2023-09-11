from django.urls import path
from order import views

urlpatterns = [
    path('order', views.order, name='order'),
    path('orderHistory', views.orderHistory, name='orderHistory'),
    path('invoice/<id>', views.invoice, name='invoice'),
]