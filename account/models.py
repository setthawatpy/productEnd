from django.db import models
from django.contrib.auth.models import User


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
    status = models.BooleanField(default=True)                      
    
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
    id = models.CharField(max_length=13, primary_key=True)         
    first_name = models.CharField(max_length=255)                   
    last_name = models.CharField(max_length=255)                    
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)   
    birthdate = models.DateField(default=None)                      
    address = models.TextField()                                    
    phone_number = models.CharField(max_length=10)                  
    profile1 = models.ImageField(upload_to='profile_customers/')     
    profile2 = models.ImageField(upload_to='profile_customers/')     
    status = models.BooleanField(default=True)                    
    
    def set_active(self, status):
        self.status = status
        self.save()
    
    def __str__(self):
        return str(self.id) + ":" + self.first_name + ":" + self.last_name+ ":" + self.phone_number