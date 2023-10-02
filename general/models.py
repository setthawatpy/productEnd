from django.db import models

# Create your models here.
# class Product(models.Model):
#     id    = models.AutoField(primary_key=True)
#     name  = models.CharField(max_length = 100) 
#     info  = models.CharField(max_length = 100, default = '')
#     price = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return self.name + self.info + str(self.price)


class Shop(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=255, blank=True, null=True)