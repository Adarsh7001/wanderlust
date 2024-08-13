from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings
from hotel.models import Hotel
from package.models import Package
from guide.models import Guide
# Create your models here.
class CustomUser(AbstractUser):
    phone=models.BigIntegerField(default=0)

    def __str__(self):
        return self.username

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.TextField(max_length=20)
    subject=models.CharField(max_length=40)
    message=models.TextField(max_length=500)

    def __str__(self):
        return self.name



class Booking(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,null=True,blank=True)
    package=models.ForeignKey(Package,on_delete=models.CASCADE,null=True,blank=True)
    guide=models.ForeignKey(Guide,on_delete=models.CASCADE,null=True,blank=True)
    service_type=models.CharField(max_length=50)
    service_id=models.PositiveIntegerField()
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=250)
    phone=models.CharField(max_length=15)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    order_id=models.CharField(max_length=100)
    payment_status=models.CharField(default='pending',max_length=30)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    razorpay_payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)
    def __str__(self):
        return self.name
