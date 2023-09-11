from django.contrib import admin
from product.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']  # ช่องค้นหาสินค้า

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stock', 'weight', 'charge', 'price', 'category']
    # list_editable = ['stock', 'weight', 'charge', 'price']
    list_per_page = 10
    list_filter = ['category']  # ตัวกรองรายการสินค้า
    search_fields = ['id', 'title']  # ช่องค้นหาสินค้า

# ลงทะเบียนคลาส CategoryAdmin กับโมเดล 'Category'
admin.site.register(Category, CategoryAdmin)

# ลงทะเบียนคลาส ProductAdmin กับโมเดล 'Product'
admin.site.register(Product, ProductAdmin)
