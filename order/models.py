from django.db import models
from django.contrib.auth.models import User
from pytz import timezone


class Order(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    net_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    # ฟังก์ชั่นวันที่ และเวลา
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


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    # ฟังก์ชั่นคำนวณราคาสินค้า
    def sub_charge(self):   # ค่ากำเหน็ด
        return self.charge * self.quantity

    def sub_total(self):    # ยอดรวมทั้งหมดของสินค้าต่อ 1 ชิ้น
        return (self.price * self.quantity) + self.sub_charge()
