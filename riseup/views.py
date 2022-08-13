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

def home(request):
    params={}
    startup_details=Startup.objects.all()
    params['startup_details']=startup_details
    return render(request,"home.html",params)

def signup(request):
    flag=0
    if(request.method=='POST'):
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        choice=request.POST['choice']
        currentPath=request.POST['currentPathsignIn']
        

        if len(username)<3 or len(username)>20:
            messages.warning(request, 'Username is either too long or too short')
            flag=1

        if not username.isalnum():
            messages.warning(request, 'Username should contain either alphabets or numerics')
            flag=1
        if pass1!=pass2:
            messages.warning(request, 'Password is not matching')
            flag=1
            # if choice is 1 student
        choice = int(choice)
        if(choice==1):
            signup = Student(name=fname + lname,email=email,user_type=1,username=username )
            signup.save()
            flag=0
            # print(choice)

            # if choice is 2 startup
        if(choice==2):
            signup = Startup(name=fname + lname,email=email,user_type=2,username=username )
            signup.save()
            flag=0
            # if choice is 3 investor
            # print(choice)/
        if(choice==3):
            signup = Investor(name=fname + lname,email=email,user_type=3,username=username )
            signup.save()
            flag=0
            # print(choice)
        if flag==1:
            return redirect(currentPath)
        else:
            newUser=User.objects.create_user(username,email,pass1)
            newUser.first_name=fname
            newUser.last_name=lname
            newUser.save()
            messages.success(request, 'Successfully created account')
            login(request,newUser)
            return redirect(currentPath)
    else:
        return HttpResponse('Not Found')


def userLogin(request):
    if (request.method=="POST"):
        username=request.POST['loginusername']
        userpass=request.POST['loginpass']
        currentPathlogIn=request.POST['currentPathlogIn']
        choice=request.POST['Choice']

        user=authenticate(request,username=username,password=userpass)

        if user is None:
            messages.error(request, 'Invalid credentials, Please try again')
            return redirect(currentPathlogIn)
        else:
            login(request,user)
            messages.success(request, 'Successfully Logged in')
            return redirect(currentPathlogIn)
    return HttpResponse('404 - Not found')


def userLogout(request):
    if request.method=="POST":
        currentPath=request.POST['currentPath']
    logout(request)
    messages.info(request, 'Successfully Logged out')
    return redirect(currentPath)

def startup(request,myid):
    params={}
    startup_object=Startup.objects.get(startup_id=myid)
    params['startup_object']=startup_object
    return render(request,"startup.html",params)


def request(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type', '')
        request_type = request.POST.get('request_type', '')
        description = request.POST.get('description', '')
        specific_link = request.POST.get('specific_link', '')
        status  = request.POST.get('status', '')
        finalreq = Request(user_name=request.user,user_type=user_type,request_type=request_type,description=description,specific_link=specific_link,status=status)
        finalreq.save()
    return redirect("/")


def tracker(request):
    params={}
    try:
        current_user=request.user.username
        student=Student.objects.values('username')
        investor=Investor.objects.values('username')
        startup=Startup.objects.values('username')
        for i in student:
            print(i)
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
        for i in investor:
            print(i)
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
        for i in startup:
            print(i)
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
    except Exception as e:
        print(e)
    # print(student)
    # if(Startup.objects.get(username=request.user)):
    #     params['request1']=Request.objects.filter(user_type=1)
    #     params['request3']=Request.objects.filter(user_type=3)
    #     params['user_type']=2
    # if(Investor.objects.get(username=request.user)):
    #     params['request1']=Request.objects.filter(user_type=3)
    #     params['user_type']=1
    # if(Student.objects.get(username=request.user)):
    print(params)
    
    return render(request,"tracker.html",params)