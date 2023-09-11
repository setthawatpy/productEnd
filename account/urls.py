from django.urls import path
from account import views

urlpatterns = [
    # Authenticate
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('changPassword', views.change_password, name='changPassword'),
    
    # Customers
    path('createCustomers', views.createCustomers, name='createCustomers'),
    path('editCustomers/<id>', views.editCustomers, name='editCustomers'),
    path('deleteCustomers/<id>>', views.deleteCustomers, name='deleteCustomers'),
    path('customersList', views.customersList, name='customersList'),
    path('customersProfile/<id>', views.customersProfile, name='customersProfile'),
    path('activate_customers/<id>/', views.activate_customers, name='activate_customers'),
    path('search_customers', views.search_customers, name='search_customers'),
    
    # Employees
    path('createEmployees', views.createEmployees, name='createEmployees'),
    path('editEmployees/<id>', views.editEmployees, name='editEmployees'),
    path('deleteEmployees/<id>/', views.deleteEmployees, name='deleteEmployees'),
    path('employeesList', views.employeesList, name='employeesList'),
    path('employeesProfile/<id>', views.employeesProfile, name='employeesProfile'),
    path('activate_employees/<id>/', views.activate_employees, name='activate_employees'),
    path('search_employees', views.search_employees, name='search_employees'),
] 