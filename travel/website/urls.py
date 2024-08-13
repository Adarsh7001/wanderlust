"""
URL configuration for travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
app_name='website'

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('contact/',views.contact,name='contact'),
    path('contactafter/',views.contactafter,name='contactafter'),
    path('bookservice/<str:service_type>/<int:service_id>/',views.bookservice,name='bookservice'),
    path('payment/',views.payment,name='payment'),
    path('status/<u>/',views.payment_status,name='status'),
    path('bookingsview/',views.bookings_view,name='bookings_view'),



]
from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)