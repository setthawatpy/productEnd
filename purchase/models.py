from django.db import models
from django.contrib.auth.models import User
from pytz import timezone

class Purchase(models.Model):
    GOLD_TYPES_CHOICES = [
        ('แหวนทองคำ', 'แหวนทองคำ'),
        ('สร้อยข้อมือทองคำ', 'สร้อยข้อมือทองคำ'),
        ('สร้อยคอทองคำ', 'สร้อยคอทองคำ'),
        ('กำไลทองคำ', 'กำไลทองคำ'),
        ('จี้ทองคำ', 'จี้ทองคำ'),
        ('ต่างหูทองคำ', 'ต่างหูทองคำ'),
        ('แท่งทองคำ', 'แท่งทองคำ'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    gold_type = models.CharField(max_length=255, choices=GOLD_TYPES_CHOICES)         # ประเภททองคำที่รับซ์้อ
    quantity = models.IntegerField()                                                # จำนวนที่รับซื้อ
    weight = models.DecimalField(max_digits=10, decimal_places=2)                   # น้ำหนักทองที่รับซื้อ
    price = models.DecimalField(max_digits=10, decimal_places=2)                    # ราคาทองที่รับซื้อ
    id_card = models.CharField(max_length=13)                                       # รหัสบัตรประชาชนลูกค้า
    first_name = models.CharField(max_length=255)                                   # ชื่อลูกค้า
    last_name = models.CharField(max_length=255)                                    # นามสกุลลูกค้า
    address = models.TextField(blank=True)                                          # ที่อยู่ลูกค้า
    phone_number = models.CharField(max_length=10)                                  # เบอร์โทร
    date_time = models.DateTimeField(auto_now_add=True)                             # วันที่ เวลา ที่รับซื้อ
    picture = models.ImageField(upload_to='purchase/')                              # รูปสินค้าที่รับซื้อ
    
    class Meta :
        ordering = ('id',)
        verbose_name = 'รับซื้อทองคำ'
        verbose_name_plural = "ข้อมูลรับซื้อทองคำ"
        
        
    # ฟังก์ชั่นวันที่ และเวลา
    def get_date(self):
        tz_thai = timezone('Asia/Bangkok')
        dt_thai = self.date_time.astimezone(tz_thai)
        
        # แปลง ค.ศ. เป็น พ.ศ.
        thai_year = dt_thai.year + 543
        
        return dt_thai.strftime(f'%d/%m/{thai_year}')
        # return dt_thai.strftime('%d/%m/%Y')     # วันที่ : วัน / เดือน / ปี
    
    
    def get_time(self):     
        tz_thai = timezone('Asia/Bangkok')
        dt_thai = self.date_time.astimezone(tz_thai)
        return dt_thai.strftime('%H:%M:%S')     # เวลา : ชั่วโมง / นาที / วินาที
    
    
class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)