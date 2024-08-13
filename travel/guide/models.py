from django.db import models

# Create your models here.
class Guide(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    description=models.TextField(max_length=200)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    languages=models.TextField(max_length=200)
    def __str__(self):
        return self.name