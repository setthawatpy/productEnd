from django.db import models
from account.models import Customer
from pytz import timezone
from datetime import datetime
from django.contrib.auth.models import User


class Contract(models.Model):
    PERIOD_CHOICES = [
        ('1', '1 เดือน'),
        ('2', '2 เดือน'),
        ('3', '3 เดือน'),
        ('4', '4 เดือน'),
        ('5', '5 เดือน'),
        ('6', '6 เดือน'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    period = models.CharField(max_length=255, choices=PERIOD_CHOICES)
    picture = models.ImageField(upload_to='contracts/')
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_loan = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    contract_status = models.BooleanField(default=False)
    redemption_status = models.BooleanField(default=False)

    def get_date(self):
        tz_thai = timezone('Asia/Bangkok')
        dt_thai = self.date_time.astimezone(tz_thai)

        # แปลง ค.ศ. เป็น พ.ศ.
        thai_year = dt_thai.year + 543

        # ชื่อเดือนในภาษาไทย
        thai_month_names = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
            'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ]
        thai_month = thai_month_names[dt_thai.month - 1]
        return dt_thai.strftime(f'%d {thai_month} {thai_year}')

    def get_time(self):
        tz_thai = timezone('Asia/Bangkok')
        dt_thai = self.date_time.astimezone(tz_thai)
        return dt_thai.strftime('%H:%M:%S')

    def check_payments(self):
        # เรียกดึงรายการการชำระเงินทั้งหมดสำหรับสัญญานี้ที่มีสถานะเป็น False
        unpaid = self.repayment_set.filter(status=False)
        # ถ้าไม่มีการชำระเงินที่ค้างชำระเหลืออยู่
        if not unpaid.exists():
            # ตั้งค่า status ของสัญญาเป็น True
            self.contract_status = True
            self.save()


class Item(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Repayment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    month = models.IntegerField()
    due_date = models.DateField(null=True)
    monthly_installments = models.DecimalField(max_digits=10, decimal_places=2, default=0)         
    monthly_interest = models.DecimalField(max_digits=10, decimal_places=2, default=0)            
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)              
    remaining_principal = models.DecimalField(max_digits=10, decimal_places=2, default=0)          
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='Payments/')

    def get_monthly_payment(self):
        return self.remaining_principal + self.monthly_payment
