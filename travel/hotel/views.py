from django.shortcuts import render
from hotel.models import Hotel,HotelBooking
from django.shortcuts import render
from datetime import datetime
from .models import Hotel

# Create your views here.


from datetime import datetime


from datetime import datetime
from django.shortcuts import render
from .models import Hotel, HotelBooking

from django.contrib import messages
from datetime import datetime
from django.shortcuts import render
from .models import Hotel, HotelBooking

def hotelhome(request):
    if request.method == 'POST':
        d = request.POST.get('d')
        cin = request.POST.get('cin')
        cout = request.POST.get('cout')

        if not cin or not cout:
            messages.error(request, 'Check-in and check-out dates are required.')
            return render(request, 'hotelhome.html')

        cin_date = datetime.strptime(cin, '%Y-%m-%d')
        cout_date = datetime.strptime(cout, '%Y-%m-%d')

        if cout_date <= cin_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return render(request, 'hotelhome.html')

        days_stayed = (cout_date - cin_date).days

        hotels = Hotel.objects.filter(place__icontains=d)

        for hotel in hotels:
            total_price = hotel.price * days_stayed

            # Create a HotelBooking instance
            booking = HotelBooking(
                hotel=hotel,
                check_in_date=cin_date,
                check_out_date=cout_date,
                total_price=total_price
            )
            booking.save()

        return render(request, 'hotels.html')

    return render(request, 'hotelhome.html')




def hotelview(request,i):
    h=Hotel.objects.get(id=i)
    return render(request,'hotel_view.html',{'h':h})


def hotels(request):
    hotels = Hotel.objects.filter(stock__gt=0)
    return render(request,'hotels.html')



