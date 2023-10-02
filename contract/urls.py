from django.urls import path
from contract import views

urlpatterns = [
    # Contract 6
    path('search_contract', views.search_contract, name='search_contract'),
    path('createContract', views.createContract, name='createContract'),
    path('editContract/<id>', views.editContract, name='editContract'),
    path('contract_detail/<id>', views.contract_detail, name='contract_detail'),
    path('contractsList', views.contractsList, name='contractsList'),
    
    # Contract Item 6
    path('create_item/<id>', views.create_item, name='create_item'),
    path('delete_item/<id>', views.delete_item, name='delete_item'),
    path('calculator_contract/<id>', views.calculator_contract, name='calculator_contract'),
    
    # Notification 7
    path('notificationList', views.notificationList, name='notificationList'),
    path('notification_detail/<id>', views.notification_detail, name='notification_detail'),
    path('send_line_notify', views.send_line_notify, name='send_line_notify'),
    
    
    # Payment 8
    path('paymentList', views.paymentList, name='paymentList'),
    path('payment_installment/<id>', views.payment_installment, name='payment_installment'),
    path('payment_details/<id>', views.payment_details, name='payment_details'),
    path('confirm_payment/<id>', views.confirm_payment, name='confirm_payment'),

    # Redeem 9
    path('redemption_list', views.redemption_list, name='redemption_list'),
    path('redemption_detail/<id>', views.redemption_detail, name='redemption_detail'),
    path('confirm_redemption/<id>', views.confirm_redemption, name='confirm_redemption'),
    
    
]  