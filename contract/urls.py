from django.urls import path
from contract import views

urlpatterns = [
    path('createContract', views.createContract, name='createContract'),
    path('editContract/<id>', views.editContract, name='editContract'),
    path('deleteContract/<id>', views.deleteContract, name='deleteContract'),
    path('contractList', views.contractList, name='contractList'),
    path('search_contract', views.search_contract, name='search_contract'),
    path('addItem', views.addItem, name='addItem'),
    # path('sendLineNotification', views.sendLineNotification, name='sendLineNotification'),
    
    
]