from django.urls import path
from purchase import views

urlpatterns = [
    path('createPurchases', views.createPurchases, name='createPurchases'),
    path('editPurchases/<id>', views.editPurchases, name='editPurchases'),
    path('deletePurchases/<int:id>', views.deletePurchases, name='deletePurchases'),
    path('purchasesList', views.purchasesList, name='purchasesList'),
    path('purchasesDetail/<id>', views.purchasesDetail, name='purchasesDetail'),
    path('purchaseReceipt/<id>', views.purchaseReceipt, name='purchaseReceipt'),
    path('search_purchases', views.search_purchases, name='search_purchases'),
    
    
    path('render_pdf_view/<id>', views.render_pdf_view, name='render_pdf_view'),
]