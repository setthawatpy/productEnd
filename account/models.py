from django.db import models
from django.contrib.auth.models import User

class Geographies(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Provinces(models.Model):
    name_th = models.CharField(max_length=255)
    name_th_short = models.CharField(max_length=10)
    name_en = models.CharField(max_length=255)
    geographies = models.ForeignKey(Geographies, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_th
    
class District(models.Model):
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_th
    
class Subdistrict(models.Model):
    zip_code = models.IntegerField()
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name_th
    
class Employee(models.Model):
    GENDER_CHOICES = [
        ('ชาย', 'ชาย'),
        ('หญิง', 'หญิง')
    ]
    id = models.CharField(max_length=13, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    birthdate = models.DateField(default=None)
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    profile1 = models.ImageField(upload_to='profile_employees/')
    profile2 = models.ImageField(upload_to='profile_employees/')
    status = models.BooleanField(default=True)                      # เพิ่มฟิลด์เป็น boolean
    
    def set_active(self, status):
        self.status = status
        self.save()
        
    def __str__(self):
        return self.id + ":" + self.first_name + ":" + self.last_name + ":" + self.phone_number
    
class Customer(models.Model):
    GENDER_CHOICES = [
        ('ชาย', 'ชาย'),
        ('หญิง', 'หญิง')
    ]
    id = models.CharField(max_length=13, primary_key=True)          # รหัสบัตรประชาชนลูกค้า PK
    first_name = models.CharField(max_length=255)                   # ชื่อ
    last_name = models.CharField(max_length=255)                    # นามสกุล
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)    # เพศ
    birthdate = models.DateField(default=None)                      # วันเกิด
    address = models.TextField()                                    # ที่อยู่
    phone_number = models.CharField(max_length=10)                  # เบอร์โทร
    profile1 = models.ImageField(upload_to='profile_customers/')     # รูปภาพ
    profile2 = models.ImageField(upload_to='profile_customers/')     # รูปภาพ
    status = models.BooleanField(default=True)                      # เพิ่มฟิลด์เป็น boolean
    
    def set_active(self, status):
        self.status = status
        self.save()
    
    def __str__(self):
        return str(self.id) + ":" + self.first_name + ":" + self.last_name+ ":" + self.phone_number