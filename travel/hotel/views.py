from django.shortcuts import render
from hotel.models import Hotel,HotelBooking
from django.shortcuts import render
from datetime import datetime
from .models import Hotel
from django.contrib import messages

from django.shortcuts import render
from hotel.models import Hotel, HotelBooking
from datetime import datetime
from django.contrib import messages

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

        # Query hotels that match the destination and are in stock
        hotels = Hotel.objects.filter(place__icontains=d, stock__gt=0)

        # Process bookings only if there are available hotels
        if hotels.exists():
            for hotel in hotels:
                # Check for existing bookings for the same hotel and dates
                existing_booking = HotelBooking.objects.filter(
                    hotel=hotel,
                    check_in_date=cin_date,
                    check_out_date=cout_date
                ).first()

                # Only create a booking if it doesn't exist
                if not existing_booking:
                    total_price = hotel.price * days_stayed
                    booking = HotelBooking(
                        hotel=hotel,
                        check_in_date=cin_date,
                        check_out_date=cout_date,
                        total_price=total_price
                    )
                    booking.save()
                else:
                    messages.warning(request, f'Booking already exists for {hotel.name} on these dates.')

            return render(request, 'hotels.html', {'hotel': hotels})

        else:
            messages.error(request, 'No hotels available for the specified destination.')

    return render(request, 'hotelhome.html')





def hotelview(request,i):
    h=Hotel.objects.get(id=i)
    return render(request,'hotel_view.html',{'h':h})


def hotels(request):
    return render(request,'hotels.html',)



