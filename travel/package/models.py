from django.db import models

# Create your models here.

class Package(models.Model):
    name=models.CharField(max_length=20)
    places=models.TextField(max_length=200)
    duration=models.TextField(max_length=200)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField(max_length=400)
    image=models.ImageField(upload_to='images', blank=True, null=True)
    banner=models.ImageField(upload_to='images', null=True, blank=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    services_included=models.TextField(max_length=300)
    services_excluded=models.TextField(max_length=300)
    stock=models.IntegerField()
    date_booked=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
