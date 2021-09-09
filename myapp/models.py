from os import truncate
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=40)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    pic=models.FileField(upload_to='profile/', null=True,blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    uid= models.ForeignKey(User,on_delete=models.CASCADE)
    etitle= models.CharField(max_length=50)
    edate=models.DateField()
    edis= models.TextField()
    epic=models.FileField(upload_to='Event pic', null=True,blank=True)

    def __str__(self):
        return self.uid.name + "  >  " +self.etitle


class product(models.Model):
    pdname=models.CharField(max_length=300)
    pdprice= models.IntegerField(default=25)
    pddis=models.TextField(max_length=2000)
    pdimage=models.FileField(upload_to='pdimage', null=True, blank=True)
  

