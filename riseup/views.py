from urllib import response
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib import messages
from math import ceil
from riseup.models import *
import io
import json

# Create your views here.
def index(request):
    return render(request,"index.html")

def startup(request,myid):
    params={}
    startup_object=Startup.objects.get(startup_id=myid)
    params['startup_object']=startup_object
    return render(request,"startup.html",params)