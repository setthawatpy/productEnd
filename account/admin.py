from django.contrib import admin
from account.models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    list_per_page = 10
    search_fields = ['id', 'first_name', 'last_name']
    

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    list_per_page = 10
    search_fields = ['id', 'first_name', 'last_name']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
