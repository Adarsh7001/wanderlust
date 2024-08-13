from django.shortcuts import render
from package.models import Package

# Create your views here.
def packagehome(request):
    p = Package.objects.filter(stock__gt=0)
    return render(request, 'packagehome.html', {'p': p})


def packageview(request,i):
    p=Package.objects.get(id=i)
    return render(request,'packageview.html',{'p':p})

