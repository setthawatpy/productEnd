from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)                          # รหัสตะกร้าสินค้า 
    employee = models.ForeignKey(User, on_delete=models.CASCADE, default=None)      # รหัสพนักงานที่ทำการ login อยู่ในระบบ
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)                        # รหัสตะกร้าสินค้า FK
    product = models.ForeignKey(Product, on_delete=models.CASCADE)                  # รหัสสินค้า FK
    quantity = models.IntegerField()                                                # จำนวนสินค้าในตะกร้า
    
    # ฟังก์ชั่นคำนวณราคาสินค้า
    def sub_charge(self):   # คำนวณค่ากำเหน็ด
        return self.product.charge * self.quantity
    
    
    def sub_total(self):    # คำนวณยอดรวมทั้งหมดของสินค้าต่อ 1 ชิ้น
        return (self.product.price * self.quantity) + self.sub_charge()
    
