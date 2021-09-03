from django.db import models
from django.db.models.fields import EmailField



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

