from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from website.models import CustomUser,Contact
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import razorpay
from package.models import Package
from hotel.models import Hotel,HotelBooking
from guide.models import Guide
from website.models import Booking,Payment
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.
def home(request):
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        u=request.POST.get('u')
        p=request.POST.get('p')
        user=authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('website:home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('website:user_login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        m = request.POST['m']
        f = request.POST['f']
        l = request.POST['l']

        if cp == p:
            if CustomUser.objects.filter(username=u).exists():
                messages.error(request, 'Username already exists')
                return redirect('website:register')
            else:
                user = CustomUser.objects.create_user(username=u, password=p, email=e, phone=m, first_name=f,
                                                      last_name=l)
                user.save()
                return redirect('website:home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('website:register')

    return render(request, 'register.html')


@login_required()
def user_logout(request):
    logout(request)
    return home(request)

@login_required()
def contact(request):
    if request.method=='POST':
        n=request.POST['n']
        e=request.POST['e']
        m=request.POST['m']
        s=request.POST['s']
        h=Contact.objects.create(name=n,email=e,subject=s,message=m)
        return redirect('website:contactafter.html')
    return render(request,'contact.html')
def contactafter(request):
    return render(request,'contactafter.html')


@login_required(login_url='website:user_login')
def bookservice(request, service_type, service_id):
    service = None
    total = 0

    if service_type == 'package':
        service = Package.objects.get(id=service_id)
        total = int(service.price * 100)  # Convert to paisa for Razorpay

    elif service_type == 'guide':
        service = Guide.objects.get(id=service_id)
        total = int(service.price * 100)  # Convert to paisa for Razorpay

    elif service_type == 'hotel':
        service = Hotel.objects.get(id=service_id)
        hotel_booking = HotelBooking.objects.filter(hotel=service, check_in_date__isnull=False,
                                                    check_out_date__isnull=False).first()

        if hotel_booking:
            total = int(hotel_booking.total_price * 100)  # Convert to paisa for Razorpay

    if not service:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Create Razorpay client
        client = razorpay.Client(auth=('rzp_test_PWhGmAwZRgvpt4', 'p6BwVsUsGN8gmZZSM7m3Hq8n'))

        # Create order
        response_payment = client.order.create(dict(amount=total, currency='INR'))
        order_id = response_payment['id']
        payment_status = response_payment['status']

        if payment_status == 'created':
            # Save the booking details
            booking = Booking.objects.create(
                user=request.user, service_type=service_type, service_id=service.id,
                name=name, address=address, phone=phone,
                amount=total / 100, order_id=order_id
            )
            booking.save()

            # Save the payment details
            payment = Payment.objects.create(
                name=name,
                amount=total / 100,
                order_id=order_id,
                paid=False
            )
            payment.save()

            print(f"Payment record created with Order ID: {order_id}")

        response_payment['name'] = request.user.username
        return render(request, 'payment.html', {'payment': response_payment})

    return render(request, 'bookservice.html', {'service': service, 'service_type': service_type})


@csrf_exempt
def payment_status(request, u):
    if not request.user.is_authenticated:
        user = CustomUser.objects.get(username=u)
        login(request, user)

    if request.method == 'POST':
        response = request.POST

        razorpay_order_id = response.get('razorpay_order_id')
        razorpay_payment_id = response.get('razorpay_payment_id')
        razorpay_signature = response.get('razorpay_signature')

        print(f"Looking for Payment with Order ID: {razorpay_order_id}")

        try:
            payment = Payment.objects.get(order_id=razorpay_order_id)
            client = razorpay.Client(auth=('rzp_test_PWhGmAwZRgvpt4', 'p6BwVsUsGN8gmZZSM7m3Hq8n'))
            status = client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            if status:
                payment.razorpay_payment_id = razorpay_payment_id
                payment.paid = True
                payment.save()

                user = CustomUser.objects.get(username=u)
                bookings = Booking.objects.filter(user=user, order_id=razorpay_order_id)

                for booking in bookings:
                    booking.payment_status = 'paid'
                    booking.save()

                    if booking.service_type == 'package':
                        service = Package.objects.get(id=booking.service_id)
                        if service.stock > 0:
                            service.stock -= 1
                            service.save()

                    elif booking.service_type == 'hotel':
                        service = Hotel.objects.get(id=booking.service_id)
                        hotel_booking = HotelBooking.objects.filter(hotel=service, check_in_date__isnull=False,
                                                                    check_out_date__isnull=False).first()

                        if hotel_booking:
                            payment.amount = hotel_booking.total_price
                            payment.save()

                        if service.stock > 0:
                            service.stock -= 1
                            service.save()

                return render(request, 'status.html', {'status': True})
            else:
                return render(request, 'status.html', {'status': False})

        except Payment.DoesNotExist:
            return render(request, 'status.html', {'status': False})

    return render(request, 'status.html', {'status': False})


def payment(request):
    return render(request,'payment.html')




@login_required
def bookings_view(request):
    bookings=Booking.objects.filter(user=request.user,payment_status='paid')
    return render(request, 'bookings_view.html', {'bookings': bookings})

# Create your views here.
