from django.urls import path
from dashboard import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('report_account', views.report_account, name='report_account'),
    path('report_product', views.report_product, name='report_product'),
    path('report_purchase', views.report_purchase, name='report_purchase'),
    path('report_sales', views.report_sales, name='report_sales'),
    path('report_contract', views.report_contract, name='report_contract'),
]