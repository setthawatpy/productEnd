from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)       # ชื่อหมวดหมู่สินค้า PK
    picture = models.ImageField(upload_to='category/')          # รูปภาพ
    
    class Meta :
        ordering = ('title',)
        verbose_name = 'หมวดหมู่สินค้า'
        verbose_name_plural = "ข้อมูลหมวดหมู่สินค้า"
        
    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    # รหัสหมวดหมู่สินค้า FK
    id = models.CharField(max_length=10, primary_key=True)              # รหัสสินค้า PK
    title = models.CharField(max_length=255, unique=True)               # ชื่อสินค้า 
    description = models.TextField(blank=True)                          # รายละเอียดสินค้า
    stock = models.IntegerField()                                       # จำนวนสินค้า
    weight = models.DecimalField(max_digits=10, decimal_places=2)       # น้ำหนักทอง
    charge = models.DecimalField(max_digits=10, decimal_places=2)       # ค่ากำเหน็ด
    price = models.DecimalField(max_digits=10, decimal_places=2)        # ราคาทอง
    available = models.BooleanField(default=True)                       # สถานะสินค้า
    create_datetime = models.DateTimeField(auto_now_add=True)           # วันที่เพิ่มสินค้า
    update_datetime = models.DateTimeField(auto_now=True)               # วันที่อัพเดทสินค้า
    picture1 = models.ImageField(upload_to='products/')      # รูปภาพ
    picture2= models.ImageField(upload_to='products/', blank=True)      # รูปภาพ
    picture3 = models.ImageField(upload_to='products/', blank=True)      # รูปภาพ
    picture4 = models.ImageField(upload_to='products/', blank=True)      # รูปภาพ
    picture5 = models.ImageField(upload_to='products/', blank=True)      # รูปภาพ
    
    class Meta :
        ordering=('title',)
        verbose_name='สินค้า'
        verbose_name_plural="ข้อมูลสินค้า"
        
    # ฟังก์ชั่นคำนวณราคาสินค้า
    def sub_total(self):
        return self.price + self.charge
    
    def __str__(self):
        return self.id + ":" + self.title + ":" + str(self.stock) + ":" + str(self.weight) + ":" + str(self.price) 