from django.shortcuts import render
from guide.models import Guide

# Create your views here.
def guidehome(request):
    guide=Guide.objects.all()
    return render(request,'guidehome.html',{'g':guide})


def guideview(request,i):
    guide=Guide.objects.get(id=i)
    return render(request,'guideview.html',{'gd':guide})