from django.contrib import admin
from purchase.models import *

# Register your models here.
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_time']
    # list_editable = []
    list_per_page = 10
    search_fields = ['id', 'date_time']

admin.site.register(Purchase, PurchaseAdmin)