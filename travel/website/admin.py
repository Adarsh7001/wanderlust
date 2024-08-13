from django.contrib import admin
from website.models import CustomUser,Contact,Booking,Payment
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Contact)
admin.site.register(Booking)
admin.site.register(Payment)