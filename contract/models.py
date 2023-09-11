from django.db import models
from account.models import Customer
from pytz import timezone
from decimal import Decimal

# Create your models here.
class Contract(models.Model):
    PERIOD_CHOICES = [
        ('1', '1 เดือน'),
        ('2', '2 เดือน'),
        ('3', '3 เดือน'),
        ('4', '4 เดือน'),
        ('5', '5 เดือน'),
        ('6', '6 เดือน'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    # ข้อมูลลูกค้า
    date_time = models.DateTimeField(auto_now_add=True)                 # วันที่
    title = models.CharField(max_length=255)                            # ประเภททอง
    weight = models.DecimalField(max_digits=10, decimal_places=2)       # น้ำหนักทอง                  
    price = models.DecimalField(max_digits=10, decimal_places=2)        # ราคาทอง
    period = models.CharField(max_length=255, choices=PERIOD_CHOICES)   # งวดที่ต้องการชำระต่อเดือน
    picture = models.ImageField(upload_to='contract/', blank=True)      # รูปภาพ
    
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
    
class ContractItem(models.Model):
    title = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)   # น้ำหนักทอง                  # น้ำหนักทองที่รับซื้อ
    price = models.DecimalField(max_digits=10, decimal_places=2)    # ราคาทอง
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    