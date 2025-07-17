from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'store/index.html')

def about(request):
    return HttpResponse("we are at about")

def contact(request):
    return HttpResponse("we are at contact")

def tracker(request):
    return HttpResponse("we are at traker")

def search(request):
    return HttpResponse("we are at search")

def productView(request):
    return HttpResponse("we are at productView")

def checkout(request):
    return HttpResponse("we are at checkout")

