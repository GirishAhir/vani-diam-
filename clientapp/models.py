from django.db import models
from django.db.models.fields import EmailField
from django.http import request
from myapp.models import product
from django.contrib.auth import get_user_model




# Create your models here.

class client(models.Model):
    clname=models.CharField(max_length=100)
    clemail=models.EmailField(max_length=40)
    clmob=models.CharField(max_length=20)
    cladd= models.TextField(max_length=400)
    compname=models.CharField(max_length=100)
    position=models.CharField(max_length=50)
    clpassword= models.CharField(max_length=100)
    role=models.CharField(default='client', max_length=50)


    def __str__(self):
        return self.clname + ' :' + self.compname 
    

class Sale(models.Model):
    created = models.DateTimeField()
    product = models.ForeignKey(product, on_delete=models.PROTECT)



class Transaction(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)










