from django.db import models
from django.contrib.auth.models import AbstractUser
class Hotel(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    hotel_image=models.ImageField(upload_to='images', blank=True, null=True)
    room_image=models.ImageField(upload_to='images', blank=True, null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    room_amenities=models.TextField()
    maximum_number_of_guests=models.IntegerField()
    stock=models.IntegerField()
    description=models.TextField(max_length=300)

    def __str__(self):
        return self.name
class HotelBooking(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    check_in_date=models.DateTimeField(blank=True, null=True)
    check_out_date=models.DateTimeField(blank=True, null=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)











